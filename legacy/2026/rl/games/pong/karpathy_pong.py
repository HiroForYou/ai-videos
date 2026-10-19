"""
Helper module for the Reinforcement learning video (karpathy pong).

Public API
| Name | Type |
|---|---|
| `git_commit` | function |
| `new_run_dir` | function |
| `latest_run_dir` | function |
| `ckpt_compatible` | function |
| `prepro` | function |
| `new_stack` | function |
| `push_frame` | function |
| `sigmoid` | function |
| `policy_forward` | function |
| `policy_backward` | function |
| `entropy_and_grad` | function |
| `discount_rewards` | function |
| `rolling` | function |
| `summary` | function |
| `save_run` | function |
| `save_plot` | function |
| `save_checkpoint` | function |
| `render_progress` | function |
"""
import json
import os
import pickle
import subprocess
import sys
import time
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import gymnasium as gym
import ale_py

gym.register_envs(ale_py)

ENV_ID = "ALE/Pong-v5"
H = 200
NUM_FRAMES = 4              # stack last N frames instead of a single frame-diff
D_FRAME = 80 * 80
D = NUM_FRAMES * D_FRAME
BATCH_SIZE = 10
LEARNING_RATE = 1e-4
GAMMA = 0.99
DECAY_RATE = 0.99
ENTROPY_BETA = 0.01        # entropy bonus to keep exploration alive
SEED = 0
RESUME = True
RENDER = False
SAVE_EVERY = 25
PROGRESS_EVERY = 200

ALGO = "karpathy"
GAME = "pong"
UP, DOWN = 2, 3

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = os.path.join(HERE, "runs", ALGO)
os.makedirs(RUNS_DIR, exist_ok=True)


def git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=HERE,
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None


def new_run_dir():
    path = os.path.join(RUNS_DIR, datetime.now().strftime("run_%Y%m%d_%H%M%S"))
    os.makedirs(path)
    return path


def latest_run_dir():
    runs = sorted(r for r in os.listdir(RUNS_DIR)
                  if os.path.isdir(os.path.join(RUNS_DIR, r)))
    return os.path.join(RUNS_DIR, runs[-1]) if runs else None


def ckpt_compatible(path):
    try:
        d = pickle.load(open(path, "rb"))
        return d["model"]["W1"].shape == (H, D)
    except Exception:
        return False


resume_dir = latest_run_dir() if RESUME else None
resume_ckpt = os.path.join(resume_dir, "checkpoint.p") if resume_dir else None
have_ckpt = bool(resume_ckpt and os.path.exists(resume_ckpt)
                 and ckpt_compatible(resume_ckpt))
if resume_dir and not have_ckpt and resume_ckpt and os.path.exists(resume_ckpt):
    print("Latest run checkpoint is a different architecture; starting fresh run.")
run_dir = resume_dir if have_ckpt else new_run_dir()
print(f"Run: {run_dir}")

checkpoint_file = os.path.join(run_dir, "checkpoint.p")
best_checkpoint_file = os.path.join(run_dir, "best_checkpoint.p")
run_file = os.path.join(run_dir, "run.json")
plot_file = os.path.join(run_dir, "plot.png")
progress_dir = os.path.join(run_dir, "progress")
os.makedirs(progress_dir, exist_ok=True)

np.random.seed(SEED)

meta = {
    "game": GAME,
    "algo": ALGO,
    "framework": "numpy",
    "description": "Karpathy policy gradients: manual backprop, discounted "
                   "normalized per-step returns, batched RMSProp; "
                   f"{NUM_FRAMES}-frame stacking, entropy bonus",
    "env_id": ENV_ID,
    "actions": [UP, DOWN],
    "action_meanings": ["UP", "DOWN"],
    "D": D,
    "H": H,
    "num_frames": NUM_FRAMES,
    "learning_rate": LEARNING_RATE,
    "batch_size": BATCH_SIZE,
    "gamma": GAMMA,
    "decay_rate": DECAY_RATE,
    "entropy_beta": ENTROPY_BETA,
    "optimizer": "rmsprop",
    "seed": SEED,
    "started_at": datetime.now().isoformat(timespec="seconds"),
    "git_commit": git_commit(),
    "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                 "gymnasium": gym.__version__, "ale_py": ale_py.__version__},
}

if have_ckpt:
    data = pickle.load(open(checkpoint_file, "rb"))
    model = data["model"]
    rmsprop_cache = data["rmsprop_cache"]
    running_reward = data["running_reward"]
    best_reward = data.get("best_reward", -21.0)
    episode_number = data["episode_number"]
    total_steps = data.get("total_steps", 0)
    elapsed_offset = data.get("elapsed_s", 0.0)
    episodes = []
    if os.path.exists(run_file):
        prev = json.load(open(run_file))
        episodes = prev.get("episodes", [])
        meta = prev.get("meta", meta)
    print(f"Resumed ep {episode_number}, running reward {running_reward:.2f}")
else:
    model = {"W1": np.random.randn(H, D) / np.sqrt(D),
             "W2": np.random.randn(H) / np.sqrt(H)}
    rmsprop_cache = {k: np.zeros_like(v) for k, v in model.items()}
    running_reward = None
    best_reward = -21.0
    episode_number = 0
    total_steps = 0
    elapsed_offset = 0.0
    episodes = []

grad_buffer = {k: np.zeros_like(v) for k, v in model.items()}


def prepro(I):
    I = I[35:195]
    I = I[::2, ::2, 0]
    I[I == 144] = 0
    I[I == 109] = 0
    I[I != 0] = 1
    return I.astype(np.float64).ravel()


def new_stack():
    return [np.zeros(D_FRAME) for _ in range(NUM_FRAMES)]


def push_frame(stack, frame):
    stack.append(frame)
    stack.pop(0)
    return np.concatenate(stack)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def policy_forward(x):
    h = np.dot(model["W1"], x)
    h[h < 0] = 0
    p = sigmoid(np.dot(model["W2"], h))
    return p, h


def policy_backward(eph, epdlogp, epx):
    dW2 = np.dot(eph.T, epdlogp).ravel()
    dh = np.outer(epdlogp, model["W2"])
    dh[eph <= 0] = 0
    dW1 = np.dot(dh.T, epx)
    return {"W1": dW1, "W2": dW2}


def entropy_and_grad(P):
    # P: (N,) prob of UP. Bernoulli entropy H = -(p log p + (1-p) log(1-p)).
    # dH/dlogit = p(1-p) * log((1-p)/p)
    p = np.clip(P, 1e-12, 1 - 1e-12)
    H = -(p * np.log(p) + (1 - p) * np.log(1 - p))
    gradH = p * (1 - p) * np.log((1 - p) / p)
    return H, gradH


def discount_rewards(r):
    discounted = np.zeros_like(r)
    running_add = 0.0
    for t in reversed(range(len(r))):
        if r[t] != 0:
            running_add = 0
        running_add = running_add * GAMMA + r[t]
        discounted[t] = running_add
    return discounted


def rolling(x, k=100):
    out, s, q = [], 0.0, []
    for v in x:
        q.append(v); s += v
        if len(q) > k:
            s -= q.pop(0)
        out.append(s / len(q))
    return out


def summary(elapsed):
    rewards = [e["reward"] for e in episodes]
    recent = rewards[-100:]
    eps_s = episode_number / elapsed if elapsed > 0 else 0.0
    steps_s = total_steps / elapsed if elapsed > 0 else 0.0
    return {
        "episodes": episode_number,
        "total_steps": total_steps,
        "running_reward": running_reward,
        "best_reward": best_reward,
        "mean_reward_last_100": float(np.mean(recent)) if recent else None,
        "max_reward": float(np.max(rewards)) if rewards else None,
        "min_reward": float(np.min(rewards)) if rewards else None,
        "elapsed_s": elapsed,
        "episodes_per_sec": eps_s,
        "steps_per_sec": steps_s,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_run(elapsed):
    json.dump({"meta": meta, "summary": summary(elapsed), "episodes": episodes},
              open(run_file, "w"), indent=2)


def save_plot():
    if not episodes:
        return
    ep = [e["episode"] for e in episodes]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    ax = axes[0]
    ax.plot(ep, [e["reward"] for e in episodes], alpha=0.25, color="steelblue", label="reward")
    ax.plot(ep, [e["running_reward"] for e in episodes], color="steelblue", lw=2, label="running reward")
    ax.set_title("episode reward"); ax.set_xlabel("episode"); ax.legend()
    ax = axes[1]
    ax.plot(ep, rolling([e["ep_steps"] for e in episodes]), color="slateblue")
    ax.set_title("episode length (rolling-100)"); ax.set_xlabel("episode")
    ax = axes[2]
    ax.plot(ep, rolling([e.get("entropy", 0.0) for e in episodes]), color="darkorange")
    ax.set_title("policy entropy (rolling-100)"); ax.set_xlabel("episode")
    fig.suptitle(f"Karpathy Pong - numpy RMSProp, {NUM_FRAMES}-frame stack, "
                 "entropy bonus")
    fig.tight_layout()
    fig.savefig(plot_file, dpi=120)
    plt.close(fig)


def save_checkpoint(elapsed, is_best=False):
    data = {
        "model": model, "rmsprop_cache": rmsprop_cache,
        "running_reward": running_reward, "best_reward": best_reward,
        "episode_number": episode_number, "total_steps": total_steps,
        "elapsed_s": elapsed,
        "algo": ALGO, "env_id": ENV_ID, "H": H, "D": D, "num_frames": NUM_FRAMES,
    }
    pickle.dump(data, open(checkpoint_file, "wb"))
    if is_best:
        pickle.dump(data, open(best_checkpoint_file, "wb"))


_progress_env = None


def render_progress():
    global _progress_env
    import imageio.v2 as imageio
    if _progress_env is None:
        _progress_env = gym.make(ENV_ID, render_mode="rgb_array")
    obs, _ = _progress_env.reset()
    stack = new_stack()
    frames = [_progress_env.render()]
    steps = 0
    while True:
        x = push_frame(stack, prepro(obs))
        aprob, _ = policy_forward(x)
        action = UP if np.random.uniform() < aprob else DOWN
        obs, _, term, trunc, _ = _progress_env.step(action)
        steps += 1
        if steps % 3 == 0:
            frames.append(_progress_env.render())
        if term or trunc or steps > 4000:
            break
    imageio.mimsave(os.path.join(progress_dir, f"ep_{episode_number:06d}.gif"),
                    frames, fps=30)


env = gym.make(ENV_ID, render_mode="human" if RENDER else None)
observation, _ = env.reset(seed=SEED)
stack = new_stack()
xs, hs, dlogps, aps, drs = [], [], [], [], []
reward_sum = 0.0
ep_steps = 0
last_grad_norm = 0.0
start_time = time.time()

print(f"{ENV_ID} | H={H} D={D} ({NUM_FRAMES}x{D_FRAME}) lr={LEARNING_RATE} "
      f"batch={BATCH_SIZE} gamma={GAMMA} beta={ENTROPY_BETA} | RMSProp + discount")

try:
    while True:
        x = push_frame(stack, prepro(observation))

        aprob, h = policy_forward(x)
        action = UP if np.random.uniform() < aprob else DOWN

        xs.append(x)
        hs.append(h)
        aps.append(aprob)
        y = 1 if action == UP else 0
        dlogps.append(y - aprob)

        observation, reward, terminated, truncated, _ = env.step(action)
        reward_sum += reward
        ep_steps += 1
        total_steps += 1
        drs.append(reward)

        if terminated or truncated:
            episode_number += 1

            epx = np.vstack(xs)
            eph = np.vstack(hs)
            epdlogp = np.array(dlogps, dtype=np.float64)
            eparp = np.array(aps, dtype=np.float64)
            epr = np.array(drs, dtype=np.float64)
            xs, hs, dlogps, aps, drs = [], [], [], [], []

            discounted_epr = discount_rewards(epr)
            discounted_epr -= discounted_epr.mean()
            discounted_epr /= discounted_epr.std() + 1e-8

            ent_per_step, gradH = entropy_and_grad(eparp)
            epdlogp *= discounted_epr
            epdlogp += ENTROPY_BETA * gradH
            grad = policy_backward(eph, epdlogp, epx)
            for k in model:
                grad_buffer[k] += grad[k]

            if episode_number % BATCH_SIZE == 0:
                gsq = 0.0
                for k, v in model.items():
                    g = grad_buffer[k]
                    gsq += float(np.sum(g * g))
                    rmsprop_cache[k] = DECAY_RATE * rmsprop_cache[k] + (1 - DECAY_RATE) * g ** 2
                    model[k] += LEARNING_RATE * g / (np.sqrt(rmsprop_cache[k]) + 1e-5)
                    grad_buffer[k] = np.zeros_like(v)
                last_grad_norm = float(np.sqrt(gsq))

            running_reward = reward_sum if running_reward is None \
                else 0.99 * running_reward + 0.01 * reward_sum
            is_best = running_reward > best_reward
            if is_best:
                best_reward = running_reward

            elapsed = elapsed_offset + (time.time() - start_time)
            eps_s = episode_number / elapsed if elapsed > 0 else 0.0
            steps_s = total_steps / elapsed if elapsed > 0 else 0.0

            episodes.append({
                "episode": episode_number, "total_steps": total_steps,
                "ep_steps": ep_steps, "reward": reward_sum,
                "running_reward": running_reward, "best_reward": best_reward,
                "entropy": float(ent_per_step.mean()),
                "grad_norm": last_grad_norm, "elapsed_s": elapsed,
                "eps_per_sec": eps_s, "steps_per_sec": steps_s,
            })

            print(f"ep {episode_number:5d} | reward {reward_sum:+5.0f} | "
                  f"running {running_reward:6.2f} | best {best_reward:6.2f} | "
                  f"H {ent_per_step.mean():.3f} | {steps_s:5.0f} steps/s")

            if episode_number % SAVE_EVERY == 0:
                save_checkpoint(elapsed, is_best=is_best)
                save_run(elapsed)
                save_plot()
            elif is_best:
                save_checkpoint(elapsed, is_best=True)

            if episode_number % PROGRESS_EVERY == 0:
                render_progress()

            reward_sum = 0.0
            ep_steps = 0
            observation, _ = env.reset()
            stack = new_stack()

except KeyboardInterrupt:
    print(f"\nInterrupted at episode {episode_number}")
finally:
    elapsed = elapsed_offset + (time.time() - start_time)
    save_checkpoint(elapsed)
    save_run(elapsed)
    save_plot()
    render_progress()
    env.close()
    if _progress_env is not None:
        _progress_env.close()
    print(f"Saved -> {run_dir}")
