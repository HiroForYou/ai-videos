/** 2D helpers for the decision-boundary plots. */
export type Point = readonly [number, number];

/** Clip the square [-L, L]^2 to the half-plane w0*x + w1*y + b >= 0 (Sutherland-Hodgman, one edge). */
export const halfPlane = (w0: number, w1: number, b: number, L: number): Point[] => {
	const square: Point[] = [
		[-L, -L],
		[L, -L],
		[L, L],
		[-L, L],
	];
	const f = ([x, y]: Point) => w0 * x + w1 * y + b;
	const out: Point[] = [];
	for (let i = 0; i < square.length; i++) {
		const a = square[i];
		const c = square[(i + 1) % square.length];
		const fa = f(a);
		const fc = f(c);
		if (fa >= 0) {
			out.push(a);
		}
		if (fa >= 0 !== fc >= 0) {
			const t = fa / (fa - fc);
			out.push([a[0] + t * (c[0] - a[0]), a[1] + t * (c[1] - a[1])]);
		}
	}
	return out;
};

/** Endpoints of the line w0*x + w1*y + b = 0 inside [-L, L]^2 (w1 != 0). */
export const boundaryLine = (w0: number, w1: number, b: number, L: number): [Point, Point] => {
	const y = (x: number) => -(w0 * x + b) / w1;
	return [
		[-L, y(-L)],
		[L, y(L)],
	];
};

export const classify = (w0: number, w1: number, b: number, [x, y]: Point) => (w0 * x + w1 * y + b >= 0 ? 1 : -1);
