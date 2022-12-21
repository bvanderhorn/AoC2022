"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
function contains(array, element) {
    return array.filter(el => {
        if (el.length != element.length)
            return false;
        for (let i = 0; i < el.length; i++)
            if (el[i] !== element[i])
                return false;
        return true;
    }).length >= 1;
}
function expand(coor1, coor2) {
    var varIndex = (coor1[0] === coor2[0]) ? 1 : 0;
    var start = Math.min(coor1[varIndex], coor2[varIndex]);
    var end = Math.max(coor1[varIndex], coor2[varIndex]);
    var varIndices = Array(end - start + 1).fill(1).map((_, index) => start + index);
    var expanded = (coor1[0] === coor2[0]) ? varIndices.map(el => [coor1[0], el]) : varIndices.map(el => [el, coor1[1]]);
    return start === coor1[varIndex] ? expanded : expanded.reverse();
}
function expandTrace(trace) {
    var expTrace = [trace[0]];
    for (let i = 1; i < trace.length; i++)
        expTrace = expTrace.concat(expand(trace[i - 1], trace[i]).slice(1));
    return expTrace;
}
function rockCoor(pos) {
    return [pos[0] - xMin, pos[1] - yMin];
}
function inRock(pos) {
    return pos[0] >= xMin && pos[0] <= xMax && pos[1] >= yMin && pos[1] <= yMax;
}
function isFree(pos) {
    return (!inRock(pos)) || [a, d].includes(rockString[rockCoor(pos)[1]][rockCoor(pos)[0]]);
}
function finish(down, left, right) {
    return (!inRock(down)) ||
        ((!isFree(down)) && (!inRock(left))) ||
        ((!isFree(down)) && (!isFree(left)) && (!inRock(right))) ||
        (!isFree(dropPos));
}
function next(down, left, right) {
    if (inRock(down) && isFree(down))
        return down;
    if (inRock(left) && isFree(left))
        return left;
    if (inRock(right) && isFree(right))
        return right;
    return null;
}
// params
const dropPos = [500, 0];
const d = '+';
const r = '#';
const a = '.';
const s = 'o';
const part = 1;
// parse
const input = fs.readFileSync('traces.txt', 'utf8');
const traces = input.split('\r\n').map(el => el.split('->').map(co => co.trim().split(',').map(num => +num)));
// console.log(stringify(traces.slice(0,2)));
// build rock
var rock = [];
traces.forEach(trace => expandTrace(trace).forEach(co => {
    if (!contains(rock, co))
        rock.push(co);
}));
// convert to string array
var xMin = Math.min(...rock.map(el => el[0]));
var xMax = Math.max(...rock.map(el => el[0]));
var yMin = 0;
var yMax = Math.max(...rock.map(el => el[1]));
// add floor for part 2
if (part === 2) {
    var add = (yMax + 2);
    for (let i = -add; i <= add; i++)
        rock.push([dropPos[0] + i, yMax + 2]);
    yMax += 2;
    xMin = Math.min(xMin, dropPos[0] - add);
    xMax = Math.max(xMax, dropPos[0] + add);
}
/////
var rockString = [];
for (let i = yMin; i <= yMax; i++) {
    rockString.push(Array(xMax - xMin + 1).fill(1).map((_, index) => {
        if ((index + xMin) === dropPos[0] && i === dropPos[1])
            return d;
        if (contains(rock, [index + xMin, i]))
            return r;
        return a;
    }));
}
fs.writeFileSync('rock' + (part === 2 ? '_part2' : '') + '.txt', rockString.map(el => el.join('')).join('\r\n'));
// drop sands
var finished = false;
var sands = 0;
while (!finished) {
    var curPos = dropPos;
    while (true) {
        let down = [curPos[0], curPos[1] + 1];
        let left = [curPos[0] - 1, curPos[1] + 1];
        let right = [curPos[0] + 1, curPos[1] + 1];
        let nextPos = next(down, left, right);
        finished = finish(down, left, right);
        if (finished)
            break;
        if (nextPos === null) {
            rockString[rockCoor(curPos)[1]][rockCoor(curPos)[0]] = s;
            break;
        }
        curPos = nextPos;
    }
    if (!finished) {
        sands++;
        if (sands % (part === 2 ? 1000 : 100) === 0)
            console.log(" " + sands + " sands");
    }
}
console.log(" " + sands + " sands");
fs.writeFileSync("rock_" + sands + (part === 2 ? '_part2' : '') + ".txt", rockString.map(el => el.join('')).join('\r\n'));
//# sourceMappingURL=day14.js.map