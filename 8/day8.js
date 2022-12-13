"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const input = fs.readFileSync('trees.txt', 'utf8');
console.log(input);
const lines = input.split('\r\n').map(el => el.split('').map(e => +e));
// console.log(lines);
function max(array) {
    return (array.length === 0) ? 0 : Math.max(...array);
}
function visible(row, col) {
    var left = col === 0 ? [] : lines[row].slice(0, col);
    var right = col === (lines[row].length - 1) ? [] : lines[row].slice(col + 1);
    var up = [];
    if (row != 0)
        for (const line of lines.slice(0, row))
            up.push(line[col]);
    var down = [];
    if (row != lines.length - 1)
        for (const line of lines.slice(row + 1))
            down.push(line[col]);
    return lines[row][col] > Math.min(...[max(left), max(right), max(up), max(down)]);
}
;
var nofVisible = 0;
for (let i = 0; i < lines.length; i++) {
    for (let j = 0; j < lines[0].length; j++) {
        if (visible(i, j))
            nofVisible++;
    }
}
console.log(nofVisible);
//# sourceMappingURL=day8.js.map