import * as fs from "fs";
import { cursorTo } from "readline";
type Valve = {
    name: string,
    rate: number,
    to: string[]
}
type Flow = {
    name: string, 
    minute: number,
    rate: number,
    flow: number
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
function nextValve(current:Valve, visited:string[]) : Valve {
    // if not all tunnel valves (TV) visited: sort unvisited TV on rate desc, return first
    // else: sort TV on amount of unvisited TV desc, return first
    var unv = unvisited(current.to,visited);
    if (unv.length > 0) {
        let unvisitedOnRateDesc = unv.map(v=>getValve(v)).sort((a,b) => a.rate > b.rate ? -1 : 1);
        console.log("   not all visited, sort on rate desc: " + JSON.stringify(unvisitedOnRateDesc.map(v=>{return {n:v.name,r:v.rate}})));

        return unvisitedOnRateDesc[0];
    }
    else {
        let sortedOnUnvisitedTVDesc = current.to.map(v=>getValve(v)).sort((a,b) => unvisited(a.to,visited).length > unvisited(b.to,visited).length ? -1 : 1);
        console.log("   all visited, sort on unvisited TV desc: " + JSON.stringify(sortedOnUnvisitedTVDesc.map(v=>{return {n:v.name,unv:unvisited(v.to,visited).length}})));
        return sortedOnUnvisitedTVDesc[0];
    }
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
        to: vMatch[3].split(',').map(n => n.trim()).sort()
    }
}).sort((a,b) => a.name < b.name ? -1 : 1);
// console.log(valves.map(v=>JSON.stringify(v)).slice(0,3).join('\r\n'));
fs.writeFileSync('valves_sorted.txt',valves.map(v=>JSON.stringify(v)).join('\r\n'));

var visited: string[] = [start];
var flow: Flow[] = [];
var cur = getValve(start);
for (let m=1;m<=minutes;m++) {
    console.log(" minute " + m + ", at " + cur.name + " (r " + cur.rate + "): ");
    if (cur.rate === 0 || flow.map(f=>f.name).includes(cur.name)) {
        // if rate is 0 or valve already opened: move to next valve
        if (cur.rate === 0) console.log("   rate is 0");
        if (flow.map(f=>f.name).includes(cur.name)) console.log("   already opened");
        cur = nextValve(cur,visited);
        if (!visited.includes(cur.name)) visited.push(cur.name);
        console.log("   move to " + cur.name);
    } else {
        // else: open valve and count future flow
        let fl = (minutes-m)*cur.rate;
        flow.push({
            name:cur.name,
            minute:m,
            rate: cur.rate,
            flow: fl
        });
        console.log("   open and count flow " + (minutes-m) + "*"+cur.rate+" = " + fl );
    }
}
console.log("total flow: " + flow.map(f=>f.flow).reduce((a,b)=> a+b,0));
fs.writeFileSync("flow.txt",stringify(flow));
