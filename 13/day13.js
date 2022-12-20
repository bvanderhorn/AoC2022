"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
function getNextBlock(str) {
    let ls = 0;
    let rs = 0;
    for (var i = 0; i < str.length; i++) {
        let cur = str.slice(i, i + 1);
        if (cur === l)
            ls++;
        if (cur === r)
            rs++;
        if (ls == rs && cur === sep)
            return str.slice(0, i);
        ;
    }
    return str;
}
function splitInBlocks(str) {
    let rem = str;
    var out = [];
    while (rem.length > 0) {
        let nextBlock = getNextBlock(rem);
        out.push(nextBlock);
        rem = rem.slice(nextBlock.length + 1, rem.length);
    }
    return out;
}
function parse(str) {
    if (str.slice(0, 1) === l) {
        var out = [];
        var elements = splitInBlocks(str.slice(1, str.length - 1));
        for (const el of elements)
            out.push(parse(el));
        return out;
    }
    else {
        return +str;
    }
}
function isOrderCorrect(pair) {
    let left = pair[0];
    let right = pair[1];
    for (let i = 0; i < left.length; i++) {
        if (i >= right.length)
            return 'false';
        if (typeof (left[i]) === 'number' && typeof (right[i]) === 'number') {
            if (left[i] === right[i])
                continue;
            return (left[i] < right[i]).toString();
        }
        let leftI = typeof (left[i]) === 'number' ? [left[i]] : left[i];
        let rightI = typeof (right[i]) === 'number' ? [right[i]] : right[i];
        let sub = isOrderCorrect([leftI, rightI]);
        if (sub != 'equal')
            return sub;
    }
    if (left.length < right.length)
        return 'true';
    return 'equal';
}
// params
const l = '[';
const r = ']';
const sep = ',';
// parse
const input = fs.readFileSync('packets.txt', 'utf8');
const pairs = input.split('\r\n\r\n').map(el => el.split('\r\n'));
console.log(pairs.slice(0, 3));
console.log(stringify(parse(pairs[0][0])));
// compare
var count = 0;
for (let i = 0; i < pairs.length; i++) {
    let left = parse(pairs[i][0]);
    let right = parse(pairs[i][1]);
    let isCorrect = isOrderCorrect([left, right]);
    console.log(" pair " + i + ": " + isCorrect);
    if (isCorrect != 'false')
        count += i + 1;
}
console.log("Sum of indices of correctly ordered pairs: " + count);
// part 2
// params
const div1 = '[[2]]';
const div2 = '[[6]]';
var packets = input.replace(/\r\n\r\n/g, '\r\n').split('\r\n');
packets.push(div1);
packets.push(div2);
// console.log(packets.slice(packets.length-10, packets.length));
var sortedPackets = packets.map(el => parse(el)).sort((a, b) => isOrderCorrect([a, b]) === 'true' ? -1 : 1);
console.log(sortedPackets.slice(0, 10).map(el => JSON.stringify(el)));
var dividerIndices = sortedPackets.map(el => JSON.stringify(el)).map((el, index) => [div1, div2].includes(el) ? index + 1 : -1).filter(el => el >= 0);
console.log(dividerIndices);
console.log("decoder key: " + dividerIndices[0] * dividerIndices[1]);
//# sourceMappingURL=day13.js.map