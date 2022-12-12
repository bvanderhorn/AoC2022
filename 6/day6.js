"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const input = fs.readFileSync('input.txt', 'utf8');
// console.log(input);
const inputArray = input.split('');
const packageLength = 14;
const packageIndices = inputArray.map((el, index) => {
    const sub = inputArray.slice(index - (packageLength - 1), index + 1);
    return (index >= (packageLength - 1) && sub.length === [...new Set(sub)].length) ? index : 0;
}).filter(el => el > 0);
console.log(packageIndices[0] + 1);
//# sourceMappingURL=day6.js.map