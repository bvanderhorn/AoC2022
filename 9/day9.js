"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const input = fs.readFileSync('motions.txt', 'utf8');
// console.log(input);
const motions = input.split('\r\n').map(el => el.split(' ')).map(el => [el[0], +el[1]]);
console.log(motions.slice(1610, 1630));
//# sourceMappingURL=day9.js.map