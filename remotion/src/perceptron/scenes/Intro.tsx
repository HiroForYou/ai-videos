import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';

export const Intro: React.FC<{readonly lang: Lang}> = ({lang}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', fontFamily, gap: 28}}>
			<div
				style={{
					fontSize: 168,
					fontWeight: 800,
					color: colors.text,
					letterSpacing: -2,
					opacity: interpolate(frame, [0, 0.8 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
					scale: interpolate(frame, [0, 1.2 * fps], [0.92, 1], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
						easing: Easing.bezier(0.16, 1, 0.3, 1),
						output: 'perceptual-scale',
					}),
				}}
			>
				{text('intro', 'title', lang)}
			</div>
			<div
				style={{
					fontSize: 64,
					fontWeight: 500,
					color: colors.sky,
					opacity: interpolate(frame, [0.8 * fps, 1.6 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
					translate: interpolate(frame, [0.8 * fps, 1.6 * fps], ['0px 24px', '0px 0px'], {
						extrapolateLeft: 'clamp',
						extrapolateRight: 'clamp',
						easing: Easing.bezier(0.16, 1, 0.3, 1),
					}),
				}}
			>
				{text('intro', 'subtitle', lang)}
			</div>
			<div
				style={{
					fontSize: 44,
					fontWeight: 600,
					color: colors.amber,
					marginTop: 24,
					opacity: interpolate(frame, [1.8 * fps, 2.6 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
				}}
			>
				{text('intro', 'credit', lang)}
			</div>
		</AbsoluteFill>
	);
};
