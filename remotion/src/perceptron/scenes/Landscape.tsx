import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Equation} from '../../components/Equation';
import {RichText} from '../../components/RichText';
import {SceneHeader} from '../../components/SceneHeader';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';

/** OR data from the legacy scene: (x0, x1, y). Bias fixed at b = 1. */
const DATA: [number, number, number][] = [
	[-1, -1, -1],
	[-1, 1, 1],
	[1, -1, 1],
	[1, 1, 1],
];
/** Squared error of the weighted sum z = w0 x0 + w1 x1 + 1 over the four examples. */
const error = (w0: number, w1: number) => DATA.reduce((sum, [x0, x1, y]) => sum + (y - (w0 * x0 + w1 * x1 + 1)) ** 2, 0);
const W_MIN = -1.5;
const W_MAX = 2.5;
const E_MAX = 20;

/** Gradient descent on E(w0, w1 = 1) = 3(w0 - 1)^2 + (w0 + 1)^2, dE/dw0 = 8 w0 - 4. */
const DESCENT = (() => {
	const steps = [-1.2];
	for (let i = 0; i < 7; i++) {
		const w = steps[steps.length - 1];
		steps.push(w - 0.07 * (8 * w - 4));
	}
	return steps;
})();

const lerpHex = (a: string, b: string, t: number) => {
	const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
	const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
	return `rgb(${pa.map((v, i) => Math.round(v + (pb[i] - v) * t)).join(',')})`;
};
const heightColor = (e: number) => {
	const t = Math.min(1, e / 14);
	return t < 0.5 ? lerpHex(colors.emerald, colors.sky, t * 2) : lerpHex(colors.sky, colors.muted, (t - 0.5) * 2);
};

const panelStyle: React.CSSProperties = {
	background: colors.panel,
	border: `3px solid ${colors.panelStroke}`,
	borderRadius: 28,
	overflow: 'hidden',
};

const CurvePanel: React.FC<{readonly width: number; readonly height: number}> = ({width, height}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const pad = {l: 90, r: 40, t: 40, b: 70};
	const x = (w: number) => pad.l + ((w - W_MIN) / (W_MAX - W_MIN)) * (width - pad.l - pad.r);
	const y = (e: number) => height - pad.b - (e / E_MAX) * (height - pad.t - pad.b);
	const dots = Array.from({length: 41}, (_, i) => W_MIN + (i * (W_MAX - W_MIN)) / 40);
	const drawn = interpolate(frame, [0.5 * fps, 2.5 * fps], [0, dots.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const stepT = interpolate(frame, [3 * fps, 6 * fps], [0, DESCENT.length - 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const i0 = Math.floor(stepT);
	const i1 = Math.min(DESCENT.length - 1, i0 + 1);
	const ball = DESCENT[i0] + (DESCENT[i1] - DESCENT[i0]) * Easing.bezier(0.65, 0, 0.35, 1)(stepT - i0);
	return (
		<svg width={width} height={height} style={panelStyle}>
			<line x1={pad.l} y1={y(0)} x2={width - pad.r} y2={y(0)} stroke={colors.panelStroke} strokeWidth={3} />
			<line x1={x(0)} y1={pad.t} x2={x(0)} y2={y(0)} stroke={colors.panelStroke} strokeWidth={3} />
			{[-1, 0, 1, 2].map((w) => (
				<text key={w} x={x(w)} y={y(0) + 40} textAnchor="middle" fontSize={26} fill={colors.muted} fontFamily="KaTeX_Main, serif">
					{w < 0 ? `−${-w}` : w}
				</text>
			))}
			{dots.map((w, i) => (
				<circle key={w} cx={x(w)} cy={y(error(w, 1))} r={7} fill={colors.sky} opacity={i < drawn ? 1 : 0} />
			))}
			{DESCENT.slice(0, i0 + 1).map((w) => (
				<circle key={`t${w}`} cx={x(w)} cy={y(error(w, 1))} r={6} fill={colors.amber} opacity={0.55} />
			))}
			<circle
				cx={x(ball)}
				cy={y(error(ball, 1)) - 14}
				r={16}
				fill={colors.amber}
				opacity={interpolate(frame, [2.6 * fps, 3 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}
			/>
		</svg>
	);
};

const BowlPanel: React.FC<{readonly width: number; readonly height: number}> = ({width, height}) => {
	const frame = useCurrentFrame();
	const {fps, durationInFrames} = useVideoConfig();
	const az = (interpolate(frame, [0, durationInFrames], [30, 80]) * Math.PI) / 180;
	const el = (28 * Math.PI) / 180;
	const s = 190;
	const project = (w0: number, w1: number, e: number) => {
		const X = (w0 - 0.5) / 2;
		const Y = (w1 - 0.5) / 2;
		const Z = (Math.min(e, E_MAX) / E_MAX) * 1.5;
		const xr = X * Math.cos(az) - Y * Math.sin(az);
		const yr = X * Math.sin(az) + Y * Math.cos(az);
		return {sx: width / 2 + s * xr, sy: height / 2 + 150 - s * (Z * Math.cos(el) + yr * Math.sin(el)), depth: yr};
	};
	const grid = Array.from({length: 13}, (_, i) => W_MIN + (i * (W_MAX - W_MIN)) / 12);
	const pts = grid
		.flatMap((w0) => grid.map((w1) => ({w0, w1, e: error(w0, w1)})))
		.map((p) => ({...p, ...project(p.w0, p.w1, p.e)}))
		.sort((a, b) => b.depth - a.depth);
	const appear = interpolate(frame, [0.3 * fps, 1.5 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const axisEnd = (w0: number, w1: number, e: number) => project(w0, w1, e);
	const origin = axisEnd(0.5, 0.5, 0);
	const min = project(0.5, 0.5, error(0.5, 0.5));
	return (
		<svg width={width} height={height} style={panelStyle}>
			<g opacity={appear * 0.8}>
				<line x1={origin.sx} y1={origin.sy} x2={axisEnd(2.5, 0.5, 0).sx} y2={axisEnd(2.5, 0.5, 0).sy} stroke={colors.sand} strokeWidth={3} />
				<line x1={origin.sx} y1={origin.sy} x2={axisEnd(0.5, 2.5, 0).sx} y2={axisEnd(0.5, 2.5, 0).sy} stroke={colors.sand} strokeWidth={3} />
				<line x1={origin.sx} y1={origin.sy} x2={axisEnd(0.5, 0.5, 14).sx} y2={axisEnd(0.5, 0.5, 14).sy} stroke={colors.sand} strokeWidth={3} />
			</g>
			{pts.map((p) => (
				<circle key={`${p.w0},${p.w1}`} cx={p.sx} cy={p.sy} r={5.5 - p.depth * 1.2} fill={heightColor(p.e)} opacity={appear * (p.e > E_MAX ? 0 : 0.95)} />
			))}
			<circle
				cx={min.sx}
				cy={min.sy}
				r={15}
				fill={colors.amber}
				opacity={interpolate(frame, [4.5 * fps, 5.2 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}
			/>
		</svg>
	);
};

export const Landscape: React.FC<{readonly lang: Lang; readonly title: string}> = ({lang, title}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
	const show = (start: number) => ({
		opacity: interpolate(frame, [start * fps, (start + 0.7) * fps], [0, 1], clamp),
		translate: interpolate(frame, [start * fps, (start + 0.7) * fps], ['0px 24px', '0px 0px'], {...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1)}),
	});
	return (
		<AbsoluteFill style={{fontFamily}}>
			<SceneHeader title={title} section={text('landscape', 'header', lang)} />
			<div style={{position: 'absolute', left: 140, top: 190, display: 'flex', flexDirection: 'column', gap: 18, ...show(0)}}>
				<CurvePanel width={820} height={540} />
				<RichText text={text('landscape', 'curve', lang)} size={38} color={colors.muted} mathColor={colors.text} />
			</div>
			<div style={{position: 'absolute', left: 1020, top: 190, display: 'flex', flexDirection: 'column', gap: 18, ...show(3.2)}}>
				<BowlPanel width={760} height={540} />
				<RichText text={text('landscape', 'surface', lang)} size={38} color={colors.muted} mathColor={colors.text} />
			</div>
			<div style={{position: 'absolute', left: 140, top: 870, width: 1640, display: 'flex', alignItems: 'center', justifyContent: 'space-between', ...show(5.6)}}>
				<Equation
					tex="E(w_0, w_1) = \sum_{i} \left(y_i - z_i\right)^2,\qquad z_i = w_0 x_{0,i} + w_1 x_{1,i} + b"
					size={38}
					display
					maxWidth={1000}
				/>
				<RichText text={text('landscape', 'minimum', lang)} size={38} weight={700} color={colors.amber} />
			</div>
		</AbsoluteFill>
	);
};
