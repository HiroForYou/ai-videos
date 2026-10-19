import {Composition, Folder} from 'remotion';
import {calculatePerceptronMetadata, Perceptron} from './perceptron/Perceptron';

export const RemotionRoot: React.FC = () => {
	return (
		<Folder name="Perceptron">
			<Composition
				id="PerceptronEN"
				component={Perceptron}
				durationInFrames={2400}
				fps={30}
				width={1920}
				height={1080}
				defaultProps={{lang: 'en' as const}}
				calculateMetadata={calculatePerceptronMetadata}
			/>
			<Composition
				id="PerceptronES"
				component={Perceptron}
				durationInFrames={2400}
				fps={30}
				width={1920}
				height={1080}
				defaultProps={{lang: 'es' as const}}
				calculateMetadata={calculatePerceptronMetadata}
			/>
		</Folder>
	);
};
