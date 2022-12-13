"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const input = fs.readFileSync('trees.txt', 'utf8');
// console.log(input);
const lines = input.split('\r\n').map(el => el.split('').map(e => +e));
// console.log(lines);
function max(array) {
    return (array.length === 0) ? -1 : Math.max(...array);
}
function left(row, col) {
    return col === 0 ? [] : lines[row].slice(0, col).reverse();
}
function right(row, col) {
    return col === (lines[row].length - 1) ? [] : lines[row].slice(col + 1);
}
function up(row, col) {
    var up = [];
    if (row != 0)
        for (const line of lines.slice(0, row))
            up.push(line[col]);
    return up.reverse();
}
function down(row, col) {
    var down = [];
    if (row != lines.length - 1)
        for (const line of lines.slice(row + 1))
            down.push(line[col]);
    return down;
}
function visible(row, col) {
    return lines[row][col] > Math.min(...[max(left(row, col)), max(right(row, col)), max(up(row, col)), max(down(row, col))]);
}
;
function directionScore(size, directionSizes) {
    var score = directionSizes.findIndex(el => el >= size);
    return score === -1 ? directionSizes.length : score + 1;
}
function scenicScore(row, col) {
    var tree = lines[row][col];
    var leftScore = directionScore(tree, left(row, col));
    var rightScore = directionScore(tree, right(row, col));
    var upScore = directionScore(tree, up(row, col));
    var downScore = directionScore(tree, down(row, col));
    return leftScore * rightScore * upScore * downScore;
}
var nofVisible = 0;
for (let i = 0; i < lines.length; i++) {
    for (let j = 0; j < lines[0].length; j++) {
        if (visible(i, j))
            nofVisible++;
    }
}
console.log(nofVisible);
// var row = 0;
// var col = 9;
// console.log(max(right(4,3)).toString());
// console.log(lines[row][col]);
// console.log([max(left(row,col)), max(right(row,col)), max(up(row,col)), max(down(row,col))]);
// console.log(Math.min(...[max(left(row,col)), max(right(row,col)), max(up(row,col)), max(down(row,col))]));
// console.log(visible(row,col));
// console.log(lines.length);
// console.log(lines[0].length);
var maxScenicScore = 0;
for (let i = 0; i < lines.length; i++) {
    for (let j = 0; j < lines[0].length; j++) {
        if (scenicScore(i, j) > maxScenicScore)
            maxScenicScore = scenicScore(i, j);
    }
}
console.log(maxScenicScore);
// console.log(49*49*49*49);
// var row = 13;
// var col = 10;
// console.log(lines[row][col]);
// console.log(left(row,col).toString());
// console.log(right(row,col).toString());
// console.log(up(row,col).toString());
// console.log(down(row,col).toString());
// console.log(scenicScore(13,10));
// console.log([].findIndex(el => el === 1));
//# sourceMappingURL=day8.js.map