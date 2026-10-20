"""
Regenerates the data/ inputs of the Backpropagation (part 1) scenes.

Each step reproduces the cells of the notebook that produced the file, with the
paths the scenes read and a device that falls back to CPU.

Steps
| Step | Notebook | Output (under data/backpropagation/hackin/) | Scenes |
|---|---|---|---|
| `p50` | p50_51.ipynb | p50/p50_2d.npy, .png | p50_51, p50_51_book |
| `p24_28` | p24_28.ipynb | p_24_28_losses_4.npy, _4xy.npy, _4.png | p24_28, p24v4_ai_book, p33_35* |
| `p33_35` | p33_35.ipynb | p_33_35_grads_1_2.npy, _grads_2_2.npy, _xy_2.npy | p33_35, p33_35_ai_book, p33_35_sketch |
| `curves` | p39_41_export_random_1d_all.ipynb, p39_41_export_pretrained.ipynb | apr_24_5/, apr_24_7/ | p39_48, p39_48_book, book_landscape_with_magenta_lines, poster_hackin_1 |
| `landscape` | loss_landscape_merch_ideas.ipynb | loss_landscape.npy | book_renders_2_gradient_descent.ipynb |
| `wormhole` | p47_wormhole.ipynb | wormhole_merged/000-065.npy, loss_2d_1*.png | p39_48, opening_rewrite*, thumbnail_hackin_1, book_landscape_hackin, poster_hackin_1 |
| `wikitext` | p48_training_on_wikitext.ipynb | apr_29_2/pre_step_*.npy, post_step_*.npy | p48c |

Differences with the notebooks
| Topic | Notebook | Here |
|---|---|---|
| Two-weight landscapes (`p24_28`, `p33_35`) | One full forward per grid point | Same values from the cached last-layer activations: only the final norm and lm_head are recomputed, in batches |
| 2D landscapes (`landscape`, `wormhole`, `wikitext`) | 512 x 512 grid on GPU | `--grid` points per side (default 16), upsampled to 512 x 512 with cubic interpolation |
| 1D curves | 4096 points | `--curve-points` (default 512) |
| Optimizer on CPU | Adam on every parameter (about 20 GB of RAM) | `--optimizer sign` (default without CUDA) on the first 8 layers: the Adam step for a constant gradient, without optimizer state; `--optimizer adam` keeps the original |
| Random directions | Drawn on CUDA | Drawn on the active device, so the landscapes differ from the original renders |

Model: meta-llama/Llama-3.2-1B needs an accepted license and `hf auth login`;
--model-id unsloth/Llama-3.2-1B loads the same weights without a token.

Run from the repo root
    .venv/Scripts/python legacy/2025/backprop_1/generate_inputs.py --steps p50 p24_28 p33_35
    .venv/Scripts/python legacy/2025/backprop_1/generate_inputs.py --steps all --model-id unsloth/Llama-3.2-1B
"""
import argparse
import json
import time
from collections import OrderedDict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.ndimage import zoom
from torch.nn import functional as F
from tqdm import tqdm

OUT_DIR = Path(__file__).resolve().parent / 'data' / 'backpropagation' / 'hackin'
TEXT = "The capital of France is Paris"
PARIS = 12366  # token id of ' Paris'; its position in TEXT is 6, predicted from position 5
SCENE_GRID = 512  # alphas_1 = np.linspace(-2.5, 2.5, 512) in the scenes

# Llama 3.2 1B config, only used for the randomly initialized model (p39_41_export_random_1d_all.ipynb)
LLAMA_CONFIG = {
    "architectures": ["LlamaForCausalLM"], "attention_bias": False, "attention_dropout": 0.0,
    "bos_token_id": 128000, "eos_token_id": 128001, "head_dim": 64, "hidden_act": "silu",
    "hidden_size": 2048, "initializer_range": 0.02, "intermediate_size": 8192,
    "max_position_embeddings": 131072, "mlp_bias": False, "model_type": "llama",
    "num_attention_heads": 32, "num_hidden_layers": 16, "num_key_value_heads": 8,
    "pretraining_tp": 1, "rms_norm_eps": 1e-05,
    "rope_scaling": {"factor": 32.0, "high_freq_factor": 4.0, "low_freq_factor": 1.0,
                     "original_max_position_embeddings": 8192, "rope_type": "llama3"},
    "rope_theta": 500000.0, "tie_word_embeddings": True, "torch_dtype": "float32",
    "use_cache": True, "vocab_size": 128256,
}


def save_texture(arr, path, transpose=False, vmax=None):
    """Borderless image of a loss grid, as the scenes' commented export blocks write it."""
    plt.figure(frameon=False)
    ax = plt.Axes(plt.gcf(), [0., 0., 1., 1.])
    ax.set_axis_off()
    plt.gcf().add_axes(ax)
    plt.imshow(np.rot90(arr.T if transpose else arr), vmax=vmax)
    plt.savefig(path, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()


def load_model(args, random_init=False):
    from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaConfig, LlamaForCausalLM
    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    if random_init:
        torch.manual_seed(42)
        np.random.seed(42)
        model = LlamaForCausalLM(LlamaConfig.from_dict(LLAMA_CONFIG))
    else:
        model = AutoModelForCausalLM.from_pretrained(args.model_id, dtype=torch.float32)
    model.to(args.device).eval()
    ids = tokenizer(TEXT, return_tensors='pt')['input_ids'].to(args.device)
    return model, tokenizer, ids


def paris_loss(model, ids):
    """-log p(' Paris') at position 5; positions after 5 do not affect it (causal model)."""
    logits = model(ids[:, :6], logits_to_keep=1).logits[0, -1]
    return -F.log_softmax(logits.float(), dim=-1)[PARIS].item()


# ---- p50_51.ipynb

def step_p50(args):
    x = np.linspace(-2.5, 2.5, 256)
    X, Y = np.meshgrid(x, x)
    Z = 0.2 * (X**2 + Y**2) - 1.0 * np.exp(-((X - 1.0)**2 + (Y + 1.0)**2) / 0.5)
    out = OUT_DIR / 'p50'
    out.mkdir(parents=True, exist_ok=True)
    save_texture(Z, out / 'p50_2d.png')
    np.save(out / 'p50_2d', Z)


# ---- p24_28.ipynb and p33_35.ipynb: two weights of model.layers.15.mlp.down_proj

class LastLayerProbe:
    """
    Loss as a function of two entries of the last down_proj, from one cached forward.

    Changing W[i, j] adds (w - w0) * x[t, j] to channel i of the residual stream at every
    position t. Layer 15 is the last decoder layer, so only the final RMSNorm and lm_head
    follow; their logits are linear in the two offsets up to the RMSNorm scale.
    """

    def __init__(self, model, ids, layer=15):
        self.model, self.ids = model, ids
        down = model.model.layers[layer].mlp.down_proj
        self.W = down.weight
        cache = {}
        h1 = down.register_forward_hook(lambda m, i, o: cache.__setitem__('x', i[0].detach()))
        h2 = model.model.norm.register_forward_hook(lambda m, i, o: cache.__setitem__('h', i[0].detach()))
        with torch.no_grad():
            model(ids)
        h1.remove(); h2.remove()
        self.x = cache['x'][0].float()  # (T, 8192) input of down_proj
        self.h = cache['h'][0].float()  # (T, 2048) residual stream entering the final norm
        self.norm_w = model.model.norm.weight.detach().float()
        self.eps = model.model.norm.variance_epsilon
        self.lm = model.lm_head.weight.detach().float()  # (V, 2048), tied to the embedding

    def top_gradient_entries(self, n=128):
        """Entries of W with the largest |dL/dW| for the full-sentence loss (p24_28.ipynb cell 10)."""
        self.W.requires_grad_(True)
        for p in self.model.parameters():
            if p is not self.W:
                p.requires_grad_(False)
        out = self.model(self.ids, labels=self.ids)
        grad = torch.autograd.grad(out.loss, self.W)[0].float().cpu().numpy()
        flat = np.argsort(np.abs(grad).flatten())[-n:][::-1]
        return np.column_stack(np.unravel_index(flat, grad.shape))

    def evaluate(self, i1, j1, i2, j2, xs1, xs2, with_grads=False, batch=256):
        """Paris loss on the grid xs1 x xs2 and, optionally, d(sentence loss)/dW at both entries."""
        dev = self.h.device
        w1, w2 = self.W[i1, j1].item(), self.W[i2, j2].item()
        T = self.h.shape[0]
        rows = slice(0, T) if with_grads else slice(5, 6)  # the Paris loss alone only needs position 5
        h, x = self.h[rows], self.x[rows]
        paris_row = 5 if with_grads else 0
        targets = self.ids[0, 1:T]
        losses = np.zeros((len(xs1), len(xs2)), dtype=np.float32)
        g1 = np.zeros_like(losses); g2 = np.zeros_like(losses)
        x2_all = torch.tensor(xs2, dtype=torch.float32, device=dev)
        for a, x1 in enumerate(tqdm(xs1, desc='grid')):
            for s in range(0, len(xs2), batch):
                d2 = (x2_all[s:s + batch] - w2).clone().requires_grad_(with_grads)
                d1 = torch.full_like(d2, x1 - w1).requires_grad_(with_grads)
                with torch.set_grad_enabled(with_grads):
                    hb = h.unsqueeze(0).repeat(len(d2), 1, 1)  # (B, T, 2048)
                    hb[:, :, i1] = hb[:, :, i1] + d1[:, None] * x[:, j1]
                    hb[:, :, i2] = hb[:, :, i2] + d2[:, None] * x[:, j2]
                    rms = torch.rsqrt(hb.pow(2).mean(-1, keepdim=True) + self.eps)
                    logits = (hb * rms * self.norm_w) @ self.lm.T  # (B, T, V)
                    logp = F.log_softmax(logits, dim=-1)
                    losses[a, s:s + len(d2)] = (-logp[:, paris_row, PARIS]).detach().cpu().numpy()
                    if with_grads:
                        # HF loss with labels=input_ids: mean cross entropy over the T - 1 shifted targets
                        sent = -logp[:, :T - 1].gather(-1, targets.expand(len(d2), -1)[..., None]).squeeze(-1).mean(-1)
                        gd1, gd2 = torch.autograd.grad(sent.sum(), (d1, d2))
                        g1[a, s:s + len(d2)] = gd1.cpu().numpy()
                        g2[a, s:s + len(d2)] = gd2.cpu().numpy()
        return losses, g1, g2


def two_weight_setup(args):
    model, tokenizer, ids = load_model(args)
    probe = LastLayerProbe(model, ids)
    top = probe.top_gradient_entries()
    (i1, j1), (i2, j2) = top[10], top[12]  # top_index_1=10, top_index_2=12
    return model, probe, (i1, j1, i2, j2)


def check_probe(model, probe, ids, idx, points=((0.5, 1.0), (2.0, -0.5))):
    """Compare the cached evaluation against full forwards at a few points."""
    i1, j1, i2, j2 = idx
    W = probe.W
    w1, w2 = W[i1, j1].item(), W[i2, j2].item()
    for x1, x2 in points:
        with torch.no_grad():
            W[i1, j1] = x1; W[i2, j2] = x2
            full = paris_loss(model, ids)
            W[i1, j1] = w1; W[i2, j2] = w2
        fast = probe.evaluate(i1, j1, i2, j2, [x1], [x2])[0][0, 0]
        print(f'  check ({x1}, {x2}): full forward {full:.5f}, cached {fast:.5f}')


def step_p24_28(args):
    model, probe, idx = two_weight_setup(args)
    check_probe(model, probe, probe.ids, idx)
    xs = np.arange(-1.007, 4, args.landscape_step)  # notebook: 0.005
    losses, _, _ = probe.evaluate(*idx, xs, xs)
    save_texture(losses, OUT_DIR / 'p_24_28_losses_4.png')
    np.save(OUT_DIR / 'p_24_28_losses_4xy.npy', np.vstack((xs, xs)))
    np.save(OUT_DIR / 'p_24_28_losses_4.npy', losses)


def step_p33_35(args):
    model, probe, idx = two_weight_setup(args)
    xs = np.arange(-1.007, 4, args.grads_step)  # notebook: 0.01
    _, g1, g2 = probe.evaluate(*idx, xs, xs, with_grads=True, batch=64)
    np.save(OUT_DIR / 'p_33_35_grads_1_2.npy', g1)
    np.save(OUT_DIR / 'p_33_35_grads_2_2.npy', g2)
    np.save(OUT_DIR / 'p_33_35_xy_2.npy', np.vstack((xs, xs)))


# ---- Random-direction landscapes (p39_41_export_*, p47_wormhole, p48_training_on_wikitext)

def random_direction(params, seed, device):
    """Filter-normalized Gaussian direction (get_random_directions + normalize_direction), stored in bfloat16."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    out = OrderedDict()
    for name, p in params:
        d = torch.randn_like(p.data, device=device)
        d.mul_(torch.norm(p.data) / torch.norm(d))
        out[name] = d.to(torch.bfloat16)
    return out


class Mover:
    """Moves the filtered parameters along 1 or 2 directions in place, without a copy of the originals."""

    def __init__(self, params, directions):
        self.params = OrderedDict(params)
        self.dirs = directions
        self.pos = [0.0] * len(directions)

    def move_to(self, *coords):
        with torch.no_grad():
            for k, (c, d) in enumerate(zip(coords, self.dirs)):
                delta = c - self.pos[k]
                if delta:
                    for name, p in self.params.items():
                        p.add_(d[name], alpha=delta)
                self.pos[k] = c


def snake(n):
    """Grid order that changes one coordinate per move."""
    for i in range(n):
        cols = range(n) if i % 2 == 0 else range(n - 1, -1, -1)
        for j in cols:
            yield i, j


def landscape_2d(model, ids, mover, alphas, betas):
    losses = np.zeros((len(alphas), len(betas)), dtype=np.float32)
    with torch.no_grad():
        for i, j in tqdm(list(snake(len(alphas))), desc='landscape'):
            mover.move_to(alphas[i], betas[j])
            losses[i, j] = paris_loss(model, ids)
    mover.move_to(0.0, 0.0)
    return losses


def upsample(arr, size=SCENE_GRID):
    out = zoom(arr, size / arr.shape[0], order=3)
    return out[:size, :size]


def step_curves(args):
    jobs = [('apr_24_5', 'all_execpt_embedding_random_', True, args.random_seeds),
            ('apr_24_7', 'all_execpt_embedding_pretrained_', False, args.pretrained_seeds)]
    for folder, prefix, random_init, seeds in jobs:
        model, _, ids = load_model(args, random_init=random_init)
        params = [(n, p) for n, p in model.named_parameters() if p.requires_grad][1:]  # all except embedding
        out = OUT_DIR / folder
        out.mkdir(parents=True, exist_ok=True)
        alphas = np.linspace(-2.5, 2.5, args.curve_points)
        for seed in seeds:
            mover = Mover(params, [random_direction(params, seed, args.device)])
            losses = []
            with torch.no_grad():
                for a in tqdm(alphas, desc=f'{folder} seed {seed}'):
                    mover.move_to(a)
                    losses.append(paris_loss(model, ids))
            mover.move_to(0.0)
            plt.clf(); plt.plot(alphas, losses)
            plt.savefig(out / f'{prefix}{seed}.png')
            np.save(out / f'{prefix}{seed}', np.vstack((alphas, np.array(losses))))
        del model


def make_optimizer(args, model):
    if args.optimizer == 'adam':
        return torch.optim.Adam(model.parameters(), lr=args.lr)  # every parameter, as in the notebooks
    return None


def train_step(args, model, params, optimizer, batch):
    """One update on `batch`; sign descent applies lr * sign(grad), the Adam step for a constant gradient."""
    model.train()
    out = model(**batch, labels=batch['input_ids'])
    if optimizer is not None:
        optimizer.zero_grad()
        out.loss.backward()
        optimizer.step()
    else:
        grads = torch.autograd.grad(out.loss, [p for _, p in params])
        with torch.no_grad():
            for (_, p), g in zip(params, grads):
                p.add_(torch.sign(g), alpha=-args.lr)
        del grads
    model.eval()
    return out.loss.item()


def landscape_setup(args):
    model, tokenizer, ids = load_model(args)
    all_params = [(n, p) for n, p in model.named_parameters() if p.requires_grad]
    params = all_params[1:73]  # layers_name='first_8'
    if args.optimizer == 'sign':
        for _, p in all_params[:1] + all_params[73:]:
            p.requires_grad_(False)
    mover = Mover(params, [random_direction(params, 11, args.device), random_direction(params, 111, args.device)])
    mover.move_to(-0.9, 0.05)  # alpha_shift, beta_shift: start away from the center
    mover.pos = [0.0, 0.0]  # the shifted point is the new origin (original_params_shifted)
    alphas = np.linspace(-2.5, 2.5, args.grid) + 0.9  # alphas - alpha_shift
    betas = np.linspace(-2.5, 2.5, args.grid) - 0.05  # betas - beta_shift
    return model, tokenizer, ids, params, mover, alphas, betas


def step_landscape(args):
    """Pretrained landscape centered on the original weights (loss_landscape_merch_ideas.ipynb cell 54)."""
    model, _, ids = load_model(args)
    params = [(n, p) for n, p in model.named_parameters() if p.requires_grad][1:73]  # layers_name='first_8'
    mover = Mover(params, [random_direction(params, 11, args.device), random_direction(params, 111, args.device)])
    axis = np.linspace(-2.5, 2.5, args.grid)
    losses = upsample(landscape_2d(model, ids, mover, axis, axis))
    np.save(OUT_DIR / 'loss_landscape.npy', losses)


def step_wormhole(args):
    model, tokenizer, ids, params, mover, alphas, betas = landscape_setup(args)
    optimizer = make_optimizer(args, model)
    batch = {'input_ids': ids, 'attention_mask': torch.ones_like(ids)}
    out = OUT_DIR / 'wormhole_merged'
    out.mkdir(parents=True, exist_ok=True)
    log = []
    for step in range(args.wormhole_start + args.wormhole_frames):
        if step >= args.wormhole_start:
            frame = step - args.wormhole_start
            losses = upsample(landscape_2d(model, ids, mover, alphas, betas))
            np.save(out / str(frame).zfill(3), losses)
            save_texture(losses, out / f'loss_2d_1_{frame:03d}.png', transpose=True)
            if frame == 0:
                save_texture(losses, out / 'loss_2d_1.png', transpose=True)
        loss = train_step(args, model, params, optimizer, batch)
        with torch.no_grad():
            log.append({'step': step, 'train_loss': loss, 'paris_loss': paris_loss(model, ids)})
        print(log[-1])
    (out / 'training_log.json').write_text(json.dumps(log, indent=1))


def step_wikitext(args):
    from datasets import load_dataset
    model, tokenizer, ids, params, mover, alphas, betas = landscape_setup(args)
    optimizer = make_optimizer(args, model)
    tokenizer.pad_token = tokenizer.eos_token
    ds = load_dataset("Salesforce/wikitext", "wikitext-2-v1", split='train').shuffle(seed=0)
    ds = ds.filter(lambda r: len(r['text'].strip()) > 0).select(range(args.wikitext_steps))
    out = OUT_DIR / 'apr_29_2'
    out.mkdir(parents=True, exist_ok=True)
    pre = upsample(landscape_2d(model, ids, mover, alphas, betas))
    for step, row in enumerate(ds):
        np.save(out / f'pre_step_{step:03d}', pre)
        enc = tokenizer(row['text'], padding='max_length', truncation=True, max_length=128, return_tensors='pt')
        loss = train_step(args, model, params, optimizer, {k: v.to(args.device) for k, v in enc.items()})
        post = upsample(landscape_2d(model, ids, mover, alphas, betas))
        np.save(out / f'post_step_{step:03d}', post)
        print({'step': step, 'train_loss': loss})
        pre = post


STEPS = {'p50': step_p50, 'p24_28': step_p24_28, 'p33_35': step_p33_35,
         'curves': step_curves, 'landscape': step_landscape, 'wormhole': step_wormhole,
         'wikitext': step_wikitext}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--steps', nargs='+', default=['all'], choices=['all', *STEPS])
    ap.add_argument('--model-id', default='meta-llama/Llama-3.2-1B')
    ap.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    ap.add_argument('--landscape-step', type=float, default=0.01, help='p24_28 grid spacing (notebook: 0.005)')
    ap.add_argument('--grads-step', type=float, default=0.02, help='p33_35 grid spacing (notebook: 0.01)')
    ap.add_argument('--curve-points', type=int, default=512, help='points per 1D curve (notebook: 4096)')
    ap.add_argument('--random-seeds', type=int, nargs='+', default=[51, 64], help='seeds read by the scenes')
    ap.add_argument('--pretrained-seeds', type=int, nargs='+', default=[19, 27], help='seeds read by the scenes')
    ap.add_argument('--grid', type=int, default=16, help='2D landscape points per side before upsampling to 512')
    ap.add_argument('--wormhole-start', type=int, default=64, help='training steps before the first frame (delayed_viz_start)')
    ap.add_argument('--wormhole-frames', type=int, default=66, help='frames read by the scenes (num_time_steps)')
    ap.add_argument('--wikitext-steps', type=int, default=4, help='pre/post pairs read by p48c')
    ap.add_argument('--optimizer', choices=['sign', 'adam'], default='adam' if torch.cuda.is_available() else 'sign')
    ap.add_argument('--lr', type=float, default=1e-7)
    ap.add_argument('--threads', type=int, default=None, help='torch CPU threads')
    args = ap.parse_args()
    if args.threads:
        torch.set_num_threads(args.threads)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    steps = list(STEPS) if 'all' in args.steps else args.steps
    print(f'device={args.device} model={args.model_id} out={OUT_DIR}')
    for name in steps:
        t = time.time()
        print(f'== {name}')
        STEPS[name](args)
        print(f'== {name} done in {time.time() - t:.0f} s')


if __name__ == '__main__':
    main()
