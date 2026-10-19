import React from 'react';
import {colors} from '../theme';
import {Equation} from './Equation';

type Props = {
	readonly value: number;
	/** LaTeX name shown under the dial, e.g. "w_0". */
	readonly name: string;
	readonly color?: string;
	readonly min?: number;
	readonly max?: number;
	readonly radius?: number;
	/** Highlight ring, 0-1 (e.g. while the dial is being turned). */
	readonly active?: number;
};

const SWEEP = 270; // degrees from min to max, centered on 12 o'clock

/** A knob with ticks from min to max and a needle at `value` (inspired by the legacy perceptron dials). */
export const Dial: React.FC<Props> = ({value, name, color = colors.amber, min = -2, max = 2, radius = 78, active = 0}) => {
	const size = radius * 2 + 84;
	const c = size / 2;
	const angle = (v: number) => ((v - min) / (max - min) - 0.5) * SWEEP;
	const polar = (deg: number, r: number): [number, number] => [c + r * Math.sin((deg * Math.PI) / 180), c - r * Math.cos((deg * Math.PI) / 180)];
	const ticks = Array.from({length: Math.round((max - min) / 0.25) + 1}, (_, i) => min + i * 0.25);

	return (
		<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, flexShrink: 0}}>
			<svg width={size} height={size} style={{flexShrink: 0}}>
				<circle cx={c} cy={c} r={radius + 14} fill="none" stroke={color} strokeWidth={4} opacity={active} />
				<circle cx={c} cy={c} r={radius} fill={colors.panel} stroke={colors.panelStroke} strokeWidth={4} />
				{ticks.map((t) => {
					const major = Math.abs(t - Math.round(t)) < 1e-6;
					const [x1, y1] = polar(angle(t), radius - (major ? 18 : 10));
					const [x2, y2] = polar(angle(t), radius - 3);
					return <line key={t} x1={x1} y1={y1} x2={x2} y2={y2} stroke={major ? colors.sand : colors.muted} strokeWidth={major ? 4 : 2} opacity={major ? 1 : 0.6} />;
				})}
				{ticks
					.filter((t) => Math.abs(t - Math.round(t)) < 1e-6 && Math.round(t) % 2 === 0)
					.map((t) => {
						const [x, y] = polar(angle(t), radius + 30);
						return (
							<text key={`l${t}`} x={x} y={y + 8} textAnchor="middle" fontSize={24} fill={colors.muted} fontFamily="KaTeX_Main, serif">
								{t < 0 ? `−${-t}` : t}
							</text>
						);
					})}
				<line
					x1={c}
					y1={c}
					x2={polar(angle(value), radius - 22)[0]}
					y2={polar(angle(value), radius - 22)[1]}
					stroke={color}
					strokeWidth={7}
					strokeLinecap="round"
				/>
				<circle cx={c} cy={c} r={9} fill={color} />
			</svg>
			<Equation tex={`${name} = ${value < 0 ? '-' : ''}${Math.abs(value).toFixed(2)}`} size={30} color={color} />
		</div>
	);
};
