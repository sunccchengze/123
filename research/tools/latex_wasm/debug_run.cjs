const { Worker } = require('worker_threads');
const path = require('path');
const w = new Worker(path.join(__dirname, 'driver_worker.cjs'), {
  workerData: { vendorDir: path.join(__dirname, 'vendor') },
});
w.on('message', (m) => console.log('MSG:', m.type, (m.value || '').toString().slice(0, 200)));
w.on('error', (e) => console.log('WERR:', e.message));
w.on('exit', (c) => { console.log('WEXIT:', c); process.exit(0); });
setTimeout(() => { console.log('TIMEOUT, terminating'); w.terminate(); process.exit(1); }, 90000);
