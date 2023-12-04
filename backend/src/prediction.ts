import * as child from 'child_process';

export function getPrediction(input: string) {
	return new Promise((resolve, reject) => {
		const python = child.spawn('python', ['./python/main.py', input]);
		let output = '';
		python.stdout.on('data', (data) => {
			output += data.toString();
		});
		python.stderr.on('data', (err) => {});
		python.on('close', (code) => {
			if (code !== 0) {
				reject(`Process exited with code ${code}`);
			} else {
				const lines = output.split('\n').filter(Boolean);
				const lastLine = lines[lines.length - 1].replace('\r', '');
				resolve(lastLine);
			}
		});
	});
}
