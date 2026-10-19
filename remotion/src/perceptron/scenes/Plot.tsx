import React from 'react';
import {colors} from '../../theme';
import {boundaryLine, classify, halfPlane, Point} from './geometry';

export type LabeledPoint = {readonly p: Point; readonly label: 1 | -1};

type Props = {
	readonly size: number;
	readonly points: readonly LabeledPoint[];
	/** Boundary weights; omit to hide the line and regions. */
	readonly weights?: {readonly w0: number; readonly w1: number; readonly b: number};
	readonly boundaryOpacity?: number;
	/** Point to frame with a dashed square (the example being processed). */
	readonly highlight?: Point;
	readonly style?: React.CSSProperties;
};

const L = 1.6;

/** Square plot with axes, labeled points and an optional decision boundary with shaded regions. */
export const Plot: React.FC<Props> = ({size, points, weights, boundaryOpacity = 1, highlight, style}) => {
	const px = ([x, y]: Point): [number, number] => [((x + L) / (2 * L)) * size, ((L - y) / (2 * L)) * size];
	const poly = (pts: Point[]) => pts.map((p) => px(p).join(',')).join(' ');
	return (
		<svg width={size} height={size} style={{background: colors.panel, borderRadius: 28, border: `3px solid ${colors.panelStroke}`, ...style}}>
			{weights ? (
				<g opacity={boundaryOpacity}>
					<polygon points={poly(halfPlane(weights.w0, weights.w1, weights.b, L))} fill={colors.amber} opacity={0.14} />
					<polygon points={poly(halfPlane(-weights.w0, -weights.w1, -weights.b, L))} fill={colors.sky} opacity={0.12} />
				</g>
			) : null}
			<line x1={px([-L, 0])[0]} y1={px([-L, 0])[1]} x2={px([L, 0])[0]} y2={px([L, 0])[1]} stroke={colors.panelStroke} strokeWidth={3} />
			<line x1={px([0, -L])[0]} y1={px([0, -L])[1]} x2={px([0, L])[0]} y2={px([0, L])[1]} stroke={colors.panelStroke} strokeWidth={3} />
			{weights ? (
				<line
					x1={px(boundaryLine(weights.w0, weights.w1, weights.b, L)[0])[0]}
					y1={px(boundaryLine(weights.w0, weights.w1, weights.b, L)[0])[1]}
					x2={px(boundaryLine(weights.w0, weights.w1, weights.b, L)[1])[0]}
					y2={px(boundaryLine(weights.w0, weights.w1, weights.b, L)[1])[1]}
					stroke={colors.emerald}
					strokeWidth={7}
					opacity={boundaryOpacity}
				/>
			) : null}
			{highlight ? (
				<rect
					x={px(highlight)[0] - 0.09 * size}
					y={px(highlight)[1] - 0.09 * size}
					width={0.18 * size}
					height={0.18 * size}
					rx={14}
					fill="none"
					stroke={colors.sand}
					strokeWidth={4}
					strokeDasharray="12 8"
				/>
			) : null}
			{points.map(({p, label}) => {
				const [cx, cy] = px(p);
				const wrong = weights ? classify(weights.w0, weights.w1, weights.b, p) !== label : false;
				const color = label === 1 ? colors.amber : colors.sky;
				return (
					<g key={p.join(',')}>
						{wrong ? <circle cx={cx} cy={cy} r={46} fill="none" stroke={colors.pink} strokeWidth={5} strokeDasharray="10 8" /> : null}
						<circle cx={cx} cy={cy} r={30} fill={color} />
						<text x={cx} y={cy + 13} textAnchor="middle" fontSize={44} fontWeight={800} fill={colors.panel}>
							{label === 1 ? '+' : '−'}
						</text>
					</g>
				);
			})}
		</svg>
	);
};
