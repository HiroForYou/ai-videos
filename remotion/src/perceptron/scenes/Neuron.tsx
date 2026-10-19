import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Equation} from '../../components/Equation';
import {SceneHeader} from '../../components/SceneHeader';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';

const INPUTS = [
	{tex: 'x_0', weight: 'w_0', y: 330, color: colors.sky},
	{tex: 'x_1', weight: 'w_1', y: 560, color: colors.sky},
	{tex: '1', weight: 'b', y: 790, color: colors.sand},
] as const;
const IN_X = 420;
const SUM = {x: 1000, y: 560, r: 92};
const STEP = {x: 1370, y: 560, w: 220, h: 170};
const OUT = {x: 1700, y: 560, r: 72};

/** Absolutely positioned label centered on (x, y). */
const At: React.FC<{readonly x: number; readonly y: number; readonly children: React.ReactNode; readonly style?: React.CSSProperties}> = ({
	x,
	y,
	children,
	style,
}) => (
	<div style={{position: 'absolute', left: x, top: y, translate: '-50% -50%', ...style}}>{children}</div>
);

export const Neuron: React.FC<{readonly lang: Lang; readonly title: string}> = ({lang, title}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

	return (
		<AbsoluteFill style={{fontFamily}}>
			<SceneHeader title={title} section={text('neuron', 'header', lang)} />
			<svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
				{INPUTS.map((input, i) => {
					const length = Math.hypot(SUM.x - SUM.r - IN_X, SUM.y - input.y);
					return (
						<line
							key={input.tex}
							x1={IN_X + 60}
							y1={input.y}
							x2={SUM.x - SUM.r}
							y2={SUM.y}
							stroke={input.color}
							strokeWidth={5}
							strokeLinecap="round"
							strokeDasharray={length}
							strokeDashoffset={interpolate(frame, [(1 + 0.3 * i) * fps, (2 + 0.3 * i) * fps], [length, 0], {
								...clamp,
								easing: Easing.bezier(0.65, 0, 0.35, 1),
							})}
						/>
					);
				})}
				<line
					x1={SUM.x + SUM.r}
					y1={SUM.y}
					x2={STEP.x - STEP.w / 2}
					y2={STEP.y}
					stroke={colors.text}
					strokeWidth={5}
					opacity={interpolate(frame, [3 * fps, 3.5 * fps], [0, 1], clamp)}
				/>
				<line
					x1={STEP.x + STEP.w / 2}
					y1={STEP.y}
					x2={OUT.x - OUT.r}
					y2={OUT.y}
					stroke={colors.text}
					strokeWidth={5}
					opacity={interpolate(frame, [4 * fps, 4.5 * fps], [0, 1], clamp)}
				/>
				<circle
					cx={SUM.x}
					cy={SUM.y}
					r={SUM.r}
					fill={colors.panel}
					stroke={colors.amber}
					strokeWidth={5}
					opacity={interpolate(frame, [2.4 * fps, 3 * fps], [0, 1], clamp)}
				/>
				<g opacity={interpolate(frame, [3.4 * fps, 4 * fps], [0, 1], clamp)}>
					<rect
						x={STEP.x - STEP.w / 2}
						y={STEP.y - STEP.h / 2}
						width={STEP.w}
						height={STEP.h}
						rx={22}
						fill={colors.panel}
						stroke={colors.pink}
						strokeWidth={5}
					/>
					<polyline
						points={`${STEP.x - 80},${STEP.y + 40} ${STEP.x},${STEP.y + 40} ${STEP.x},${STEP.y - 40} ${STEP.x + 80},${STEP.y - 40}`}
						fill="none"
						stroke={colors.pink}
						strokeWidth={7}
						strokeLinejoin="round"
					/>
				</g>
				<circle
					cx={OUT.x}
					cy={OUT.y}
					r={OUT.r}
					fill={colors.panel}
					stroke={colors.emerald}
					strokeWidth={5}
					opacity={interpolate(frame, [4.4 * fps, 5 * fps], [0, 1], clamp)}
				/>
			</svg>

			{INPUTS.map((input, i) => (
				<React.Fragment key={input.tex}>
					<At x={IN_X} y={input.y} style={{opacity: interpolate(frame, [0.3 * i * fps, (0.3 * i + 0.6) * fps], [0, 1], clamp)}}>
						<div
							style={{
								width: 116,
								height: 116,
								borderRadius: 999,
								background: colors.panel,
								border: `5px solid ${input.color}`,
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
							}}
						>
							<Equation tex={input.tex} size={56} color={input.color} />
						</div>
					</At>
					<At
						x={(IN_X + SUM.x) / 2}
						y={(input.y + SUM.y) / 2 - 44}
						style={{opacity: interpolate(frame, [(1.6 + 0.3 * i) * fps, (2.2 + 0.3 * i) * fps], [0, 1], clamp)}}
					>
						<Equation tex={input.weight} size={56} color={colors.amber} />
					</At>
				</React.Fragment>
			))}
			<At x={IN_X} y={210} style={{fontSize: 40, fontWeight: 600, color: colors.muted, opacity: interpolate(frame, [0, 0.6 * fps], [0, 1], clamp)}}>
				{text('neuron', 'inputs', lang)}
			</At>
			<At x={SUM.x} y={SUM.y} style={{opacity: interpolate(frame, [2.6 * fps, 3.1 * fps], [0, 1], clamp)}}>
				<Equation tex="\Sigma" size={84} color={colors.amber} />
			</At>
			<At x={SUM.x} y={SUM.y + SUM.r + 50} style={{fontSize: 40, fontWeight: 600, color: colors.muted, opacity: interpolate(frame, [2.6 * fps, 3.1 * fps], [0, 1], clamp)}}>
				{text('neuron', 'sum', lang)}
			</At>
			<At x={STEP.x} y={STEP.y + STEP.h / 2 + 50} style={{fontSize: 40, fontWeight: 600, color: colors.muted, opacity: interpolate(frame, [3.6 * fps, 4.1 * fps], [0, 1], clamp)}}>
				{text('neuron', 'step', lang)}
			</At>
			<At x={OUT.x} y={OUT.y} style={{opacity: interpolate(frame, [4.6 * fps, 5.1 * fps], [0, 1], clamp)}}>
				<Equation tex="\hat{y}" size={64} color={colors.emerald} />
			</At>
			<At x={OUT.x} y={OUT.y + OUT.r + 50} style={{fontSize: 40, fontWeight: 600, color: colors.muted, opacity: interpolate(frame, [4.6 * fps, 5.1 * fps], [0, 1], clamp)}}>
				{text('neuron', 'output', lang)}
			</At>
			<At
				x={960}
				y={960}
				style={{
					opacity: interpolate(frame, [5.6 * fps, 6.4 * fps], [0, 1], clamp),
					translate: interpolate(frame, [5.6 * fps, 6.4 * fps], ['-50% -30%', '-50% -50%'], {...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1)}),
				}}
			>
				<Equation tex="\hat{y} = \operatorname{sign}\left(w_0 x_0 + w_1 x_1 + b\right) \in \{-1, +1\}" size={60} display maxWidth={1500} />
			</At>
		</AbsoluteFill>
	);
};
