import katex from 'katex';
import 'katex/dist/katex.min.css';
import React, {useEffect, useLayoutEffect, useMemo, useRef, useState} from 'react';
import {continueRender, delayRender} from 'remotion';
import {colors} from '../theme';
import './equation.css';

type Props = {
	readonly tex: string;
	/** Font size in px; KaTeX renders math at 1.21x this size. */
	readonly size?: number;
	readonly color?: string;
	/** Display mode: limits under \sum, full-size fractions. */
	readonly display?: boolean;
	/** Shrinks the equation (CSS zoom) when its natural width exceeds this many px. */
	readonly maxWidth?: number;
	readonly style?: React.CSSProperties;
};

/** LaTeX equation rendered with KaTeX. Holds the frame until the KaTeX fonts are loaded. */
export const Equation: React.FC<Props> = ({tex, size = 56, color = colors.text, display = false, maxWidth, style}) => {
	const [handle] = useState(() => delayRender('KaTeX fonts'));
	const [fontsReady, setFontsReady] = useState(false);
	const [zoom, setZoom] = useState(1);
	const probe = useRef<HTMLSpanElement>(null);
	const html = useMemo(() => katex.renderToString(tex, {throwOnError: false, displayMode: display, output: 'html'}), [tex, display]);

	useEffect(() => {
		document.fonts.ready.then(() => setFontsReady(true));
	}, []);

	// Natural width comes from an unzoomed hidden copy; offsetWidth ignores Studio's canvas transform
	useLayoutEffect(() => {
		if (!maxWidth || !probe.current) {
			setZoom(1);
			return;
		}
		const natural = probe.current.offsetWidth;
		setZoom(natural > maxWidth ? maxWidth / natural : 1);
	}, [html, size, maxWidth, fontsReady]);

	useEffect(() => {
		if (fontsReady) {
			continueRender(handle);
		}
	}, [fontsReady, handle]);

	const inner: React.CSSProperties = {display: 'inline-block', fontSize: size, color, lineHeight: 1.2, whiteSpace: 'nowrap'};
	return (
		<span style={{display: 'inline-block', position: 'relative', ...style}}>
			<span style={{display: 'inline-block', zoom}}>
				<span style={inner} dangerouslySetInnerHTML={{__html: html}} />
			</span>
			{maxWidth ? (
				<span
					ref={probe}
					aria-hidden
					style={{...inner, position: 'absolute', left: 0, top: 0, visibility: 'hidden', pointerEvents: 'none'}}
					dangerouslySetInnerHTML={{__html: html}}
				/>
			) : null}
		</span>
	);
};
