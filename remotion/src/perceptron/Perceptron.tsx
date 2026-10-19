/**
 * "The Perceptron" explainer (EN / ES). Script: ./script.json; images: public/perceptron (legacy manimgl renders).
 * Each scene lasts as long as its narration (sectionFrames), joined with 15-frame fades.
 */
import {fade} from '@remotion/transitions/fade';
import {linearTiming, TransitionSeries} from '@remotion/transitions';
import React from 'react';
import {AbsoluteFill, CalculateMetadataFunction, useVideoConfig} from 'remotion';
import {colors, fontFamily} from '../theme';
import {Lang, sectionFrames, text, totalFrames, TRANSITION_FRAMES} from './script';
import {Boundary} from './scenes/Boundary';
import {Intro} from './scenes/Intro';
import {Landscape} from './scenes/Landscape';
import {Learning} from './scenes/Learning';
import {Limits} from './scenes/Limits';
import {Neuron} from './scenes/Neuron';
import {Summary} from './scenes/Summary';

export type PerceptronProps = {
	readonly lang: Lang;
};

export const calculatePerceptronMetadata: CalculateMetadataFunction<PerceptronProps> = ({props}) => ({
	durationInFrames: totalFrames(props.lang, 30),
});

export const Perceptron: React.FC<PerceptronProps> = ({lang}) => {
	const {fps} = useVideoConfig();
	const title = text('intro', 'title', lang);
	const fadeTiming = linearTiming({durationInFrames: TRANSITION_FRAMES});

	return (
		<AbsoluteFill style={{backgroundColor: colors.bg, fontFamily}}>
			<TransitionSeries>
				<TransitionSeries.Sequence name="Intro" durationInFrames={sectionFrames('intro', lang, fps)}>
					<Intro lang={lang} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Neuron" durationInFrames={sectionFrames('neuron', lang, fps)}>
					<Neuron lang={lang} title={title} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Boundary" durationInFrames={sectionFrames('boundary', lang, fps)}>
					<Boundary lang={lang} title={title} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Learning" durationInFrames={sectionFrames('learning', lang, fps)}>
					<Learning lang={lang} title={title} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Landscape" durationInFrames={sectionFrames('landscape', lang, fps)}>
					<Landscape lang={lang} title={title} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Limits" durationInFrames={sectionFrames('limits', lang, fps)}>
					<Limits lang={lang} title={title} />
				</TransitionSeries.Sequence>
				<TransitionSeries.Transition presentation={fade()} timing={fadeTiming} />
				<TransitionSeries.Sequence name="Summary" durationInFrames={sectionFrames('summary', lang, fps)}>
					<Summary lang={lang} />
				</TransitionSeries.Sequence>
			</TransitionSeries>
		</AbsoluteFill>
	);
};
