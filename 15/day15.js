"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
function overlaps(interval1, interval2) {
    return interval1[0] <= interval2[1] && interval1[1] >= interval2[0];
}
function merge(i1, i2) {
    return [Math.min(i1[0], i2[0]), Math.max(i1[1], i2[1])];
}
function sortAndReduce(intervals, min, max) {
    var sorted = intervals.sort((a, b) => a[0] < b[0] ? -1 : 1);
    return sorted.filter(i => overlaps(i, [min, max])).map(i => [Math.max(i[0], min), Math.min(i[1], max)]);
}
function mergeIntervals(intervals) {
    var merged = intervals;
    while (true) {
        let newMerged = [];
        for (const interval of merged) {
            var didMerge = false;
            for (let i = 0; i < newMerged.length; i++) {
                if (overlaps(interval, newMerged[i])) {
                    newMerged[i] = merge(interval, newMerged[i]);
                    didMerge = true;
                    break;
                }
            }
            if (!didMerge)
                newMerged.push(interval);
        }
        if (newMerged.length < merged.length)
            merged = newMerged;
        else
            break;
    }
    return merged;
}
function GetNonBeaconStretches(line) {
    var stretches = [];
    for (const sensor of sbPositions) {
        let stretch = Math.abs(sensor[1][0] - sensor[0][0]) + Math.abs(sensor[1][1] - sensor[0][1]);
        let yDist = Math.abs(sensor[0][1] - line);
        let dx = stretch - yDist;
        if (dx >= 0)
            stretches.push([sensor[0][0] - dx, sensor[0][0] + dx]);
    }
    return stretches;
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
// console.log(stringify(sbPositions));
var sensorsOnLine = [];
var beaconsOnLine = [];
var nonBeaconStretches = GetNonBeaconStretches(yLine);
for (const sensor of sbPositions) {
    if (sensor[0][1] == yLine)
        sensorsOnLine.push(sensor[0][0]);
    if (sensor[1][1] == yLine)
        beaconsOnLine.push(sensor[1][0]);
}
sensorsOnLine = [...new Set(sensorsOnLine)];
beaconsOnLine = [...new Set(beaconsOnLine)];
var nonBeacons = mergeIntervals(nonBeaconStretches).map(interval => interval[1] - interval[0] + 1).reduce((a, b) => a + b, 0) - beaconsOnLine.length;
console.log(" merged non-beacon stretches: " + JSON.stringify(mergeIntervals(nonBeaconStretches)));
console.log(" sensors: " + sensorsOnLine);
console.log(" beacons: " + beaconsOnLine);
console.log(" non-beacon places on line " + yLine + ": " + nonBeacons);
// part 2 
const xMin = 0;
const xMax = 4000000;
const yMin = 0;
const yMax = 4000000;
const multiplier = 4000000;
for (let i = yMin; i < yMax; i++) {
    let stretches = sortAndReduce(mergeIntervals(GetNonBeaconStretches(i)), xMin, xMax);
    if (stretches.length > 1) {
        console.log(" y = " + i + " : " + JSON.stringify(stretches));
        console.log(" tuning frequency: " + ((stretches[0][1] + 1) * multiplier + i));
        break;
    }
    if (i % Math.floor((yMax - yMin + 1) / 100) == 0)
        console.log("" + (i / (yMax - yMin + 1) * 100).toPrecision(2) + "% done");
}
//# sourceMappingURL=day15.js.map