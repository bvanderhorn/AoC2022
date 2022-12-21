"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
// params
var yLine = 2000000;
// parse
const input = fs.readFileSync('sensors.txt', 'utf8');
const sensors = input.split('\r\n');
const sbPositions = sensors.map(line => {
    var mtch = line.match(/^\s*Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)\s*$/);
    return [[+mtch[1], +mtch[2]], [+mtch[3], +mtch[4]]];
});
console.log(stringify(sbPositions));
//# sourceMappingURL=day15.js.map