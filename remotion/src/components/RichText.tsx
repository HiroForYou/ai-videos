import React from 'react';
import {colors} from '../theme';
import {Equation} from './Equation';

type Props = {
	/** Plain text with inline math between dollar signs, e.g. "nudge $w_0$ by 0.1". */
	readonly text: string;
	readonly size: number;
	readonly color?: string;
	readonly mathColor?: string;
	readonly weight?: number;
	readonly style?: React.CSSProperties;
};

/** KaTeX math is 1.21x the surrounding font size; this factor keeps inline math at text height. */
const INLINE_MATH_SCALE = 0.88;

export const RichText: React.FC<Props> = ({text, size, color = colors.text, mathColor, weight = 500, style}) => (
	<span style={{fontSize: size, color, fontWeight: weight, lineHeight: 1.3, ...style}}>
		{text.split(/(\$[^$]+\$)/).map((part, i) =>
			part.startsWith('$') && part.endsWith('$') ? (
				<Equation key={i} tex={part.slice(1, -1)} size={size * INLINE_MATH_SCALE} color={mathColor ?? color} />
			) : (
				<React.Fragment key={i}>{part}</React.Fragment>
			),
		)}
	</span>
);
