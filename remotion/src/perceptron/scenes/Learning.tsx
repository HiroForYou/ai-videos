import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Dial} from '../../components/Dial';
import {Equation} from '../../components/Equation';
import {RichText} from '../../components/RichText';
import {SceneHeader} from '../../components/SceneHeader';
import {colors, fontFamily} from '../../theme';
import {Lang, text} from '../script';
import {LabeledPoint, Plot} from './Plot';

const OR_POINTS: LabeledPoint[] = [
	{p: [-1, -1], label: -1},
	{p: [-1, 1], label: 1},
	{p: [1, -1], label: 1},
	{p: [1, 1], label: 1},
];

/**
 * One perceptron update on the example x = (-1, -1), y = -1, with eta = 0.25.
 * Before: w = (-1, 1), b = 1 -> z = 1, y_hat = +1 (wrong).
 * Update: dw_i = eta (y - y_hat) x_i = 0.25 * (-2) * (-1) = +0.5; db = 0.25 * (-2) * 1 = -0.5.
 * After: w = (-0.5, 1.5), b = 0.5 -> z = -0.5, y_hat = -1 (correct); (1, -1) becomes the next mistake.
 */
const BEFORE = {w0: -1, w1: 1, b: 1};
const DELTA = {w0: 0.5, w1: 0.5, b: -0.5};

const f = (v: number) => (v < 0 ? `-${Math.abs(v).toFixed(2)}` : v.toFixed(2));

export const Learning: React.FC<{readonly lang: Lang; readonly title: string}> = ({lang, title}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
	const turn = interpolate(frame, [6 * fps, 8 * fps], [0, 1], {...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1)});
	const w0 = BEFORE.w0 + DELTA.w0 * turn;
	const w1 = BEFORE.w1 + DELTA.w1 * turn;
	const b = BEFORE.b + DELTA.b * turn;
	const z = -w0 - w1 + b;
	const active = interpolate(frame, [5.6 * fps, 6 * fps, 8 * fps, 8.4 * fps], [0, 1, 1, 0], clamp);
	const fixed = frame >= 8.2 * fps;
	const show = (start: number) => ({
		opacity: interpolate(frame, [start * fps, (start + 0.6) * fps], [0, 1], clamp),
		translate: interpolate(frame, [start * fps, (start + 0.6) * fps], ['0px 18px', '0px 0px'], {
			...clamp,
			easing: Easing.bezier(0.16, 1, 0.3, 1),
		}),
	});

	return (
		<AbsoluteFill style={{fontFamily}}>
			<SceneHeader title={title} section={text('learning', 'header', lang)} />
			<Plot
				size={540}
				points={OR_POINTS}
				weights={{w0, w1, b}}
				highlight={[-1, -1]}
				style={{position: 'absolute', left: 140, top: 190, ...show(0)}}
			/>
			<div style={{position: 'absolute', left: 110, top: 750, width: 640, display: 'flex', justifyContent: 'space-between', ...show(0.4)}}>
				<Dial name="w_0" value={w0} radius={58} active={active} />
				<Dial name="w_1" value={w1} radius={58} active={active} />
				<Dial name="b" value={b} radius={58} color={colors.sand} active={active} />
			</div>

			<div style={{position: 'absolute', left: 830, top: 200, width: 950, display: 'flex', flexDirection: 'column', gap: 30}}>
				<div style={show(0.6)}>
					<RichText text={text('learning', 'example', lang)} size={44} mathColor={colors.sky} />
				</div>
				<div style={show(1.6)}>
					<Equation
						tex={`z = (-1)(${f(w0)}) + (-1)(${f(w1)}) + ${f(b)} = ${f(z)}`}
						size={44}
						display
						maxWidth={980}
					/>
				</div>
				<div style={show(3)}>
					<RichText
						text={text('learning', fixed ? 'fixed' : 'wrong', lang)}
						size={44}
						weight={700}
						color={fixed ? colors.emerald : colors.pink}
					/>
				</div>
				<div
					style={{
						background: colors.panel,
						border: `3px solid ${colors.panelStroke}`,
						borderRadius: 24,
						padding: '28px 36px',
						display: 'flex',
						flexDirection: 'column',
						gap: 22,
						...show(4.2),
					}}
				>
					<RichText text={text('learning', 'rule', lang)} size={36} color={colors.muted} />
					<Equation tex="w_i \leftarrow w_i + \eta\,(y - \hat{y})\,x_i" size={48} color={colors.emerald} display maxWidth={900} />
					<div style={show(5.2)}>
						<Equation
							tex="\Delta w_0 = \Delta w_1 = 0.25\cdot(-2)\cdot(-1) = +0.5,\qquad \Delta b = -0.5"
							size={36}
							color={colors.amber}
							display
							maxWidth={850}
						/>
					</div>
				</div>
				<div style={show(9.2)}>
					<RichText text={text('learning', 'next', lang)} size={38} color={colors.muted} />
				</div>
			</div>
		</AbsoluteFill>
	);
};
