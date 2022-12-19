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
        if (ls == rs && cur === ',')
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
    //console.log(out);
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
// params
const l = '[';
const r = ']';
// parse
const input = fs.readFileSync('packets.txt', 'utf8');
const pairs = input.split('\r\n\r\n').map(el => el.split('\r\n'));
console.log(pairs.slice(0, 3));
console.log(getNextBlock('8,1,[2,3,3,[6,7,7,2,6]],[[8,10,1]],[9]],[1,7,[7,[3,6],7,7,10]]]'));
console.log(stringify(parse(pairs[0][0])));
//# sourceMappingURL=day13.js.map