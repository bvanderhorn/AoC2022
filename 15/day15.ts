import * as fs from "fs";
import { json } from "stream/consumers";
function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}
function overlaps(interval1:number[], interval2:number[]) : boolean {
    return interval1[0]<=interval2[1] && interval1[1]>=interval2[0]; 
}
function merge(i1:number[],i2:number[]) : number[] {
    return [Math.min(i1[0],i2[0]), Math.max(i1[1],i2[1])];
}
function mergeIntervals(intervals: number[][]) : number[][] {
    var merged = intervals;
    while (true) {
        let newMerged : number[][] = [];
        for (const interval of merged){
            var didMerge = false;
            for (let i=0; i<newMerged.length;i++) {
                if (overlaps(interval, newMerged[i])) {
                    newMerged[i] = merge(interval, newMerged[i]);
                    didMerge = true;
                    break;
                }
            }
            if (!didMerge) newMerged.push(interval);
        }
        if (newMerged.length < merged.length) merged = newMerged;
        else break;
    }
    return merged;
}

// params
var yLine = 2000000;

// parse
const input: string = fs.readFileSync('sensors.txt', 'utf8');
const sensors = input.split('\r\n');
const sbPositions = sensors.map(line => {
    var mtch = line.match(/^\s*Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)\s*$/);
    return [[+mtch[1],+mtch[2]], [+mtch[3],+mtch[4]]];
});
// console.log(stringify(sbPositions));
var sensorsOnLine: number[] = [];
var beaconsOnLine: number[] = [];
var nonBeaconStretches: number[][] = [];
for (const sensor of sbPositions){
    let stretch = Math.abs(sensor[1][0]-sensor[0][0]) + Math.abs(sensor[1][1]-sensor[0][1]);
    let yDist = Math.abs(sensor[0][1] - yLine);
    let dx = stretch-yDist;
    if (dx >= 0) nonBeaconStretches.push([sensor[0][0]-dx, sensor[0][0]+dx]);
    if (sensor[0][1] == yLine) sensorsOnLine.push(sensor[0][0]);
    if (sensor[1][1] == yLine) beaconsOnLine.push(sensor[1][0]);
}
sensorsOnLine = [...new Set(sensorsOnLine)];
beaconsOnLine = [...new Set(beaconsOnLine)];
var nonBeacons = mergeIntervals(nonBeaconStretches).map(interval => interval[1]-interval[0]+1).reduce((a,b) => a+b,0) - beaconsOnLine.length;

console.log(" merged non-beacon stretches: " + JSON.stringify(mergeIntervals(nonBeaconStretches)));
console.log(" sensors: " + sensorsOnLine);
console.log(" beacons: " + beaconsOnLine);
console.log(" non-beacon places on line " + yLine + ": " + nonBeacons);
