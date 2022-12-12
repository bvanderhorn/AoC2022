// npm install --save-dev typescript @types/node fs
// Ctrl + Shift + B -> watch
// >> node day7.js

import * as fs from "fs";

const input: string = fs.readFileSync('input.txt', 'utf8');
// console.log(input.slice(0,1000));
const commands : string[] = input.split('\r\n$');
// console.log(commands.slice(0,10));
const commandsSplit: string[][] = commands.map(el => el.split('\r\n'));
console.log(commandsSplit.slice(0,10));