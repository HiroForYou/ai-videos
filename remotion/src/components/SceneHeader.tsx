import React from 'react';
import {Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors, fontFamily, safe} from '../theme';

type Props = {
	readonly title: string;
	readonly section: string;
};

/** Top-left video title plus the current section name. */
export const SceneHeader: React.FC<Props> = ({title, section}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<div
			style={{
				position: 'absolute',
				top: safe.y - 40,
				left: safe.x,
				display: 'flex',
				alignItems: 'baseline',
				gap: 32,
				fontFamily,
				opacity: interpolate(frame, [0, 0.6 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
				translate: interpolate(frame, [0, 0.6 * fps], ['0px -16px', '0px 0px'], {
					extrapolateLeft: 'clamp',
					extrapolateRight: 'clamp',
					easing: Easing.bezier(0.16, 1, 0.3, 1),
				}),
			}}
		>
			<span style={{fontSize: 52, fontWeight: 800, color: colors.text}}>{title}</span>
			<span style={{fontSize: 44, fontWeight: 500, color: colors.muted}}>{section}</span>
		</div>
	);
};
