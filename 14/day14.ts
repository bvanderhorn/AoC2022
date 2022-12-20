import * as fs from "fs";

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}
function contains(array: any[][], element: any[]): boolean {
    return array.filter(el => {
        if (el.length != element.length) return false;
        for (let i=0;i<el.length;i++) if (el[i] !== element[i]) return false;
        return true;
    }).length >= 1;
}
function expand(coor1: number[], coor2: number[]) : number[][] {
    var varIndex = (coor1[0] === coor2[0]) ? 1 : 0;
    var start = Math.min(coor1[varIndex], coor2[varIndex]);
    var end = Math.max(coor1[varIndex], coor2[varIndex]);
    var varIndices = Array(end-start+1).fill(1).map((_, index) => start + index);
    var expanded = (coor1[0] === coor2[0]) ? varIndices.map(el => [coor1[0], el]) : varIndices.map(el => [el, coor1[1]]);
    return start === coor1[varIndex] ? expanded : expanded.reverse();
}
function expandTrace(trace:number[][]) : number[][] {
    var expTrace : number[][] = [trace[0]];
    for (let i=1;i<trace.length;i++) expTrace = expTrace.concat(expand(trace[i-1],trace[i]).slice(1));
    return expTrace;
}
function draw() : string[] {
    var xMin = Math.min(...rock.map(el => el[0]));
    var xMax = Math.max(...rock.map(el => el[0]));
    var yMin = 0;
    var yMax = Math.max(...rock.map(el => el[1]));
    var rockString: string[] = [];
    for (let i=yMin;i<=yMax;i++){
        rockString.push(Array(xMax-xMin+1).fill(1).map((_,index) => {
            if ((index+xMin) === dropPos[0] && i===dropPos[1]) return '+';
            if(contains(rock,[index+xMin,i])) return '#';
            return '.';
        }).join(''));
    }
    return rockString;
}

// params
const dropPos = [500,0];

// parse
const input: string = fs.readFileSync('traces.txt', 'utf8');
const traces = input.split('\r\n').map(el => el.split('->').map(co => co.trim().split(',').map(num => +num)));
// console.log(stringify(traces.slice(0,2)));

// build rock
var rock : number[][] = [];
traces.forEach(trace => expandTrace(trace).forEach(co => {
    if (!contains(rock, co)) rock.push(co);
}));
// console.log(traces[0]);
// console.log(expand(traces[0][0],traces[0][1]))
// console.log(expandTrace(traces[0]));

// draw rock
fs.writeFileSync('rock.txt',draw().join('\r\n'));
