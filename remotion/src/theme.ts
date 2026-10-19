/**
 * Shared look for the Remotion compositions: palette from assets/theme.json (shared with scenes/theme.py),
 * Plus Jakarta Sans text (same family as the Manim scenes), KaTeX math.
 *
 * | Token | Hex | Use |
 * |---|---|---|
 * | bg | #191919 | Background (cristhianwiki.com 'original' dark theme) |
 * | panel | #232323 | Cards, plots, dials |
 * | text / muted | #f1f5f9 / #cbd5e1 | Text |
 * | sky, amber, pink, emerald, sand | accents | Contrast >= 5.8:1 on bg |
 */
import {loadFont} from '@remotion/google-fonts/PlusJakartaSans';
import palette from '../../assets/theme.json';

/** Plus Jakarta Sans, the font of scenes/theme.py, loaded from Google Fonts. */
export const {fontFamily} = loadFont('normal', {
	weights: ['400', '500', '600', '700', '800'],
	subsets: ['latin', 'latin-ext'],
});

export const colors = {
	bg: palette.background,
	panel: palette.panel,
	panelStroke: palette.panelStroke,
	text: palette.text,
	muted: palette.muted,
	sky: palette.sky,
	amber: palette.amber,
	pink: palette.pink,
	emerald: palette.emerald,
	sand: palette.sand,
	primary: palette.primary,
} as const;

/** Safe area for 1920x1080 (video-layout rules scaled to the width). */
export const safe = {x: 140, y: 100} as const;
