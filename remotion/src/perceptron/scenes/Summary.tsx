import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors, fontFamily} from '../../theme';
import {Lang, textList} from '../script';

export const Summary: React.FC<{readonly lang: Lang}> = ({lang}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const lines = textList('summary', 'summary', lang);
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 44, fontFamily}}>
			{lines.map((line, i) => (
				<div
					key={line}
					style={{
						fontSize: 64,
						fontWeight: i === lines.length - 1 ? 800 : 600,
						color: i === lines.length - 1 ? colors.amber : colors.text,
						opacity: interpolate(frame, [(0.3 + 0.9 * i) * fps, (0.9 + 0.9 * i) * fps], [0, 1], {
							extrapolateLeft: 'clamp',
							extrapolateRight: 'clamp',
						}),
						translate: interpolate(frame, [(0.3 + 0.9 * i) * fps, (0.9 + 0.9 * i) * fps], ['0px 24px', '0px 0px'], {
							extrapolateLeft: 'clamp',
							extrapolateRight: 'clamp',
							easing: Easing.bezier(0.16, 1, 0.3, 1),
						}),
					}}
				>
					{line}
				</div>
			))}
		</AbsoluteFill>
	);
};
