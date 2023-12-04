import Fastify, { FastifyRequest } from 'fastify';
const fastify = Fastify({ logger: true });
import * as child from 'child_process';
import { getPrediction } from './prediction';

type Prediction = {
	text: string;
};

fastify
	.post<{ Body: Prediction }>('/post', async (request, reply) => {
		const input = request.body.text;
		let prediction = (await getPrediction(input)) as string;
		let prediction_array = JSON.parse(prediction);
		return { prediction_array };
	})
	.get('/test', async (request, reply) => {
		return { hello: 'world' };
	})
	.post<{ Body: Prediction }>('/predict', async (request, reply) => {
		const text = request.body.text;
		const payload = {
			text: text,
		};
		console.log(payload);
		const response = await fetch('http://127.0.0.1:8000/predict', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		});
		const data = await response.json();
		return data;
	});

const start = async () => {
	try {
		await fastify.listen({ port: 3000 });
	} catch (err) {
		fastify.log.error(err);
		process.exit(1);
	}
};
start();
