"use strict";
// npm install --save-dev typescript @types/node fs
// Ctrl + Shift + B -> watch
// >> node day7.js
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const input = fs.readFileSync('input.txt', 'utf8');
// console.log(input.slice(0,1000));
const commands = input.split('\r\n$');
// console.log(commands.slice(0,10));
const commandsSplit = commands.map(el => el.split('\r\n'));
console.log(commandsSplit.slice(0, 10));
//# sourceMappingURL=day7.js.map