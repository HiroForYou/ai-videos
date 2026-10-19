import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Equation} from '../../components/Equation';
import {SceneHeader} from '../../components/SceneHeader';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';
import {LabeledPoint, Plot} from './Plot';

/** Same data as the legacy perceptron scene (x0, x1 in {-1, 1}; only (-1, -1) is negative). */
const OR_POINTS: LabeledPoint[] = [
	{p: [-1, -1], label: -1},
	{p: [-1, 1], label: 1},
	{p: [1, -1], label: 1},
	{p: [1, 1], label: 1},
];

export const Boundary: React.FC<{readonly lang: Lang; readonly title: string}> = ({lang, title}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
	// w0 sweeps from -1 (two mistakes) to 1 (all points correct); w1 = b = 1 as in the legacy scene
	const w0 = interpolate(frame, [2.5 * fps, 7 * fps], [-1, 1], {...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1)});

	return (
		<AbsoluteFill style={{fontFamily}}>
			<SceneHeader title={title} section={text('boundary', 'header', lang)} />
			<Plot
				size={780}
				points={OR_POINTS}
				weights={{w0, w1: 1, b: 1}}
				boundaryOpacity={interpolate(frame, [1 * fps, 1.8 * fps], [0, 1], clamp)}
				style={{
					position: 'absolute',
					left: 200,
					top: 200,
					opacity: interpolate(frame, [0, 0.8 * fps], [0, 1], clamp),
				}}
			/>
			<div
				style={{
					position: 'absolute',
					left: 1060,
					top: 260,
					width: 720,
					display: 'flex',
					flexDirection: 'column',
					gap: 44,
					opacity: interpolate(frame, [1.2 * fps, 2 * fps], [0, 1], clamp),
				}}
			>
				<div style={{fontSize: 44, fontWeight: 600, color: colors.emerald}}>{text('boundary', 'boundary', lang)}</div>
				<Equation tex="w_0 x_0 + w_1 x_1 + b = 0" size={60} display maxWidth={720} />
				<Equation tex={`w_0 = ${w0.toFixed(2)},\\quad w_1 = 1,\\quad b = 1`} size={48} color={colors.amber} display maxWidth={720} />
				<div style={{display: 'flex', flexDirection: 'column', gap: 18, marginTop: 20}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 20, fontSize: 40, color: colors.text}}>
						<span style={{width: 40, height: 40, borderRadius: 8, background: colors.amber, opacity: 0.6}} />
						{text('boundary', 'positive', lang)}
					</div>
					<div style={{display: 'flex', alignItems: 'center', gap: 20, fontSize: 40, color: colors.text}}>
						<span style={{width: 40, height: 40, borderRadius: 8, background: colors.sky, opacity: 0.6}} />
						{text('boundary', 'negative', lang)}
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};
