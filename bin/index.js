#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
const python = process.platform === 'win32' ? 'python' : 'python3';
const packageRoot = path.resolve(__dirname, '..');

const child = spawn(python, ['-m', 'trushell', ...args], {
  stdio: 'inherit',
  cwd: packageRoot,
});

child.on('exit', (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  process.exit(code);
});

child.on('error', (err) => {
  console.error('Failed to launch TruShell CLI.');
  console.error('Make sure Python is installed and the TruShell package files are present.');
  console.error(err.message || err);
  process.exit(1);
});
