import * as fs from "fs";
import { cursorTo } from "readline";
type Valve = {
    name: string,
    rate: number,
    to: string[]
    pathmap:Distance[]
}
type Flow = {
    name: string, 
    minute: number,
    rate: number,
    flow: number
}
type Distance = {
    name:string,
    distance:number,
    rate: number,
    potential:number,
    to: string[],
    path:string[]
}
function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}
function getValve(valve:string) : Valve {
    return valves.filter(v=>v.name===valve)[0];
}
function unvisited(valves:string[],visited:string[]) : string[] {
    return valves.filter(v=> !visited.includes(v));
}
function isOpen(valve:string) : boolean {
    return flow.map(f=>f.name).includes(valve);
}
function shortestPathMap(valve:string): Distance[] {
    // returns a list of shortest paths from given valve to valves on matching 'valves' indices
    function getNearestUnvisited() : Distance {
        return dist.filter(d=> !vstd.includes(d.name)).sort((a,b)=> a.distance < b.distance ? -1 : 1)[0];
    }
    function getDist(valve:string) : Distance {
        return dist.filter(d=>d.name===valve)[0];
    }
    function getIndex(valve:string): number {
        return dist.map((d,index)=> d.name===valve ? index : -1).filter(i=> i>=0)[0];
    }

    const inf: number = 10000000000;
    var vstd : string[] = [];
    var dist: Distance[] = valves.map(v=>{
        return {
            name: v.name,
            distance: v.name === valve ? 0 : inf,
            rate: v.rate,
            potential: 0,
            to: v.to,
            path: []
        }
    });
    for (let i=0;i<dist.length;i++) {
        let current: Distance = getNearestUnvisited();
        for (const n of current.to) {
            let curDist = getDist(n).distance;
            let newDist = current.distance +1;
            if(curDist > newDist) {
                var dIndex = getIndex(n);
                dist[dIndex].distance = newDist;
                dist[dIndex].path = [];
                current.path.forEach(p => dist[dIndex].path.push(p));
                dist[dIndex].path.push(current.name);
            }
        }
        vstd.push(current.name);
    }
    // add each distance name to path and update potential
    dist.forEach(d=>{
        d.path.push(d.name);
        d.potential = (minutes-d.distance)*d.rate;
    });
    return dist.sort((a,b)=> a.potential > b.potential ? -1 : 1);
}
function highestPotential(valve:string,minute:number) : Distance {
    var distances = getValve(valve).pathmap.filter(d=>d.rate > 0 && !isOpen(d.name));
    distances.forEach(d=>d.potential = (minutes-minute-d.distance)*d.rate);
    return distances.sort((a,b) => a.potential > b.potential ? -1 : 1)[0];
}

// params
const start = "AA";
const minutes = 30;

// parse
const input: string = fs.readFileSync('valves.txt', 'utf8');
const valves: Valve[] = input.split('\r\n').map(v => {
    var vMatch = v.match(/Valve\s+(\w+)\s+has flow rate=(\d+); tunnels? leads? to valves?\s+([\s\S]+)$/);
    return {
        name: vMatch[1],
        rate: +vMatch[2],
        to: vMatch[3].split(',').map(n => n.trim()).sort(),
        pathmap: []
    }
}).sort((a,b) => a.name < b.name ? -1 : 1);

// add shortest path maps
valves.forEach(v=> v.pathmap = shortestPathMap(v.name));
fs.writeFileSync('valves_sorted.json',stringify(valves));
fs.writeFileSync("valve_AA.json",stringify(valves[0]));
var longestDistance = valves.map(v=> v.pathmap.sort((a,b)=>a.distance > b.distance ? -1 : 1)[0]).sort((a,b)=>a.distance > b.distance ? -1 : 1)[0];
// console.log(" longest distance: " + stringify(longestDistance));

var visited: string[] = [start];
var flow: Flow[] = [];
var cur = getValve(start);
for (let m=1;m<minutes;m++) {
    // Instead:
    // 1. for the current valve and the current minute, find out the path to which yet-unopened valve has the highest flow potential
    // 2. If current valve is unopened and rate > 0:
    //     a. calculate the flow potential of opening the current valve
    //     b. calculate the path with the highest flow potential if the path would continue another minute from now
    //     c. add (a) and (b) 
    //     d. if higher than (1.): open valve and continue
    //        else: move to next valve on path from (1.) and continue
    var comment = "minute " + m + ", at " + cur.name + " (r " + cur.rate + "): ";
    var hp = highestPotential(cur.name, m);
    var hpPot = hp.potential;
    // calculate current potential, add future path potential on m+1
    var hpplus = highestPotential(cur.name, m+1);
    var hppPot = hpplus.potential;
    var cp = (minutes-m)*cur.rate;
    var openBasedOnPotential : boolean = (cp+hppPot) > hpPot;
    if (cur.rate > 0 && (!isOpen(cur.name)) && openBasedOnPotential) {
        let fl = (minutes-m)*cur.rate;
        flow.push({
            name:cur.name,
            minute:m,
            rate: cur.rate,
            flow: fl
        });
        console.log(comment +"open and count flow " + (minutes-m) + "*"+cur.rate+" = " + fl );
    } else {
        // if rate is 0 or valve already opened or not worth opening valve: move to next valve on the highest-potential track
        cur = getValve(hp.path[1]);
        if (!visited.includes(cur.name)) visited.push(cur.name);
        console.log(comment +"move to " + cur.name + " (towards " + hp.name + ": dist. " + hp.distance + ", potential " + hpPot + ")");
    }
}
console.log("total flow: " + flow.map(f=>f.flow).reduce((a,b)=> a+b,0));
fs.writeFileSync("flow.json",stringify(flow));

