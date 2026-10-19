/**
 * Typed access to script.json (same schema as scenes/<video>/script.yaml).
 * Each section lasts as long as its narration at 150 words per minute, plus a short tail.
 */
import script from './script.json';

export type Lang = 'en' | 'es';
export type SectionId = (typeof script.sections)[number]['id'];

const WORDS_PER_SECOND = 2.5;
const TAIL_SECONDS = 0.8;
export const TRANSITION_FRAMES = 15;

const section = (id: SectionId) => {
	const found = script.sections.find((s) => s.id === id);
	if (!found) {
		throw new Error(`Unknown section ${id}`);
	}
	return found;
};

/** On-screen string for a section key, in the requested language. */
export const text = (id: SectionId, key: string, lang: Lang): string => {
	const entry = (section(id).text as unknown as Record<string, Record<Lang, string | string[]> | undefined>)[key];
	if (!entry) {
		throw new Error(`Missing text ${id}.${key}`);
	}
	const value = entry[lang];
	return Array.isArray(value) ? value.join('\n') : value;
};

export const textList = (id: SectionId, key: string, lang: Lang): string[] => text(id, key, lang).split('\n');

/** Section length in frames: narration time (+ transition overlap) at the given fps. */
export const sectionFrames = (id: SectionId, lang: Lang, fps: number): number => {
	const words = section(id).narration[lang].split(/\s+/).length;
	return Math.round((words / WORDS_PER_SECOND + TAIL_SECONDS) * fps) + TRANSITION_FRAMES;
};

export const sectionIds = script.sections.map((s) => s.id) as SectionId[];

export const totalFrames = (lang: Lang, fps: number): number =>
	sectionIds.reduce((sum, id) => sum + sectionFrames(id, lang, fps), 0) - TRANSITION_FRAMES * (sectionIds.length - 1);
