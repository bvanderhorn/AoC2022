import * as fs from "fs";

function log(test:boolean, print:any) {
    if (test) console.log(print);
}

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}
const test = true;

// parse input
const input: string = fs.readFileSync('map.txt', 'utf8');
const map = input.split('\r\n').map(el => el.split('').map(s => s.charCodeAt(0) - 97));
log(test, map);
const startPos = [20,0];
const endPos = [20,40];
map[startPos[0]][startPos[1]] = 0;
map[endPos[0]][endPos[1]] = 25;
// log(test, map[20]);
