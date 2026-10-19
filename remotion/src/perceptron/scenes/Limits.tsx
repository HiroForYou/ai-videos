import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {SceneHeader} from '../../components/SceneHeader';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';
import {LabeledPoint, Plot} from './Plot';

const XOR_POINTS: LabeledPoint[] = [
	{p: [-1, -1], label: -1},
	{p: [1, 1], label: -1},
	{p: [-1, 1], label: 1},
	{p: [1, -1], label: 1},
];

/** Two-layer network icon: 2 inputs, 2 hidden units, 1 output. */
const MultiLayer: React.FC<{readonly opacity: number}> = ({opacity}) => {
	const layers = [
		[150, 330],
		[150, 330],
		[240],
	];
	const xs = [40, 220, 400];
	return (
		<svg width={440} height={480} style={{opacity}}>
			{layers.slice(0, -1).map((layer, li) =>
				layer.flatMap((y1) =>
					layers[li + 1].map((y2) => (
						<line key={`${li}-${y1}-${y2}`} x1={xs[li]} y1={y1} x2={xs[li + 1]} y2={y2} stroke={colors.muted} strokeWidth={3} opacity={0.7} />
					)),
				),
			)}
			{layers.map((layer, li) =>
				layer.map((y) => (
					<circle key={`${li}-${y}`} cx={xs[li]} cy={y} r={34} fill={colors.panel} stroke={li === 2 ? colors.emerald : colors.sky} strokeWidth={5} />
				)),
			)}
		</svg>
	);
};

export const Limits: React.FC<{readonly lang: Lang; readonly title: string}> = ({lang, title}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
	// A line sweeping through orientations: some point is always on the wrong side
	const theta = interpolate(frame, [1 * fps, 7 * fps], [0.35, 2.8], clamp);
	const b = 0.35 * Math.sin(frame / (0.9 * fps));

	return (
		<AbsoluteFill style={{fontFamily}}>
			<SceneHeader title={title} section={text('limits', 'header', lang)} />
			<Plot
				size={780}
				points={XOR_POINTS}
				weights={{w0: Math.cos(theta), w1: Math.sin(theta), b}}
				boundaryOpacity={interpolate(frame, [0.8 * fps, 1.4 * fps], [0, 1], clamp)}
				style={{position: 'absolute', left: 200, top: 200, opacity: interpolate(frame, [0, 0.8 * fps], [0, 1], clamp)}}
			/>
			<div style={{position: 'absolute', left: 1100, top: 250, display: 'flex', flexDirection: 'column', gap: 26}}>
				<div style={{fontSize: 50, fontWeight: 700, color: colors.pink, opacity: interpolate(frame, [2 * fps, 2.8 * fps], [0, 1], clamp)}}>
					{text('limits', 'no_line', lang)}
				</div>
				<div style={{fontSize: 40, fontWeight: 500, color: colors.muted, opacity: interpolate(frame, [3.5 * fps, 4.3 * fps], [0, 1], clamp)}}>
					{text('limits', 'credit', lang)}
				</div>
				<div style={{fontSize: 46, fontWeight: 700, color: colors.emerald, marginTop: 30, opacity: interpolate(frame, [7.5 * fps, 8.3 * fps], [0, 1], clamp)}}>
					{text('limits', 'fix', lang)}
				</div>
				<MultiLayer opacity={interpolate(frame, [8 * fps, 9 * fps], [0, 1], clamp)} />
			</div>
		</AbsoluteFill>
	);
};
