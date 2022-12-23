"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
function writeFile(filename, content) {
    const exampleString = 'example';
    fs.writeFileSync((inputFile.includes(exampleString) ? exampleString + '_' : '') + filename, content);
}
function getValve(valve) {
    return valves.filter(v => v.name === valve)[0];
}
function shortestPathMap(valve) {
    // returns a list of shortest paths from given valve to all other valves using Dijkstra
    function getNearestUnvisited() {
        return dist.filter(d => !vstd.includes(d.name)).sort((a, b) => a.distance < b.distance ? -1 : 1)[0];
    }
    function getDist(valve) {
        return dist.filter(d => d.name === valve)[0];
    }
    function getIndex(valve) {
        return dist.map((d, index) => d.name === valve ? index : -1).filter(i => i >= 0)[0];
    }
    const inf = 10000000000;
    var vstd = [];
    var dist = valves.map(v => {
        return {
            name: v.name,
            distance: v.name === valve ? 0 : inf,
            rate: v.rate,
            potential: 0,
            to: v.to,
            path: []
        };
    });
    for (let i = 0; i < dist.length; i++) {
        let current = getNearestUnvisited();
        for (const n of current.to) {
            let curDist = getDist(n).distance;
            let newDist = current.distance + 1;
            if (curDist > newDist) {
                var dIndex = getIndex(n);
                dist[dIndex].distance = newDist;
                dist[dIndex].path = [];
                current.path.forEach(p => dist[dIndex].path.push(p));
                dist[dIndex].path.push(current.name);
            }
        }
        vstd.push(current.name);
    }
    // add each distance name to path
    dist.forEach(d => {
        d.path.push(d.name);
    });
    return dist;
}
function getMaxWithRemaining(curValve, rem, remMin, depth, main) {
    // recursive function trying each remaining valve as next to see which one will return the highest total flow
    var scores = [];
    var cur = getValve(curValve);
    for (let i = 0; i < rem.length; i++) {
        let vi = getValve(rem[i]);
        let dist = cur.pathmap.filter(p => p.name === vi.name)[0].distance;
        if (remMin - dist - 1 <= 0) {
            if (main) {
                let elephant = getMaxWithRemaining(start, rem, minutes, 0, false);
                if (elephant.length > 0) {
                    scores.push({
                        flow: elephant[0].flow,
                        path: []
                    });
                }
            }
        }
        else {
            let sc = getMaxWithRemaining(rem[i], rem.filter(v => v != vi.name), remMin - dist - 1, depth + 1, main);
            if (sc.length === 0 && main)
                sc = getMaxWithRemaining(start, rem.filter(v => v != vi.name), minutes, 0, false); // elephant
            let fl = (remMin - dist - 1) * vi.rate;
            let path = [];
            if (sc.length > 0) {
                fl += sc[0].flow;
                path = sc[0].path;
            }
            path.unshift(vi.name);
            scores.push({
                flow: fl,
                path: path
            });
        }
        if (depth === 2 && main) {
            iteration++;
            console.log(" " + (iteration / (valves.length - 1) / (valves.length - 2) / (valves.length - 3) * 100).toPrecision(4) + "% done");
        }
    }
    ;
    return scores.sort((a, b) => a.flow > b.flow ? -1 : 1);
}
// params
const inputFile = 'valves.txt';
const start = "AA";
const part = 2;
const minutes = (part === 2) ? 26 : 30;
// parse
const input = fs.readFileSync(inputFile, 'utf8');
var valves = input.split('\r\n').map(v => {
    var vMatch = v.match(/Valve\s+(\w+)\s+has flow rate=(\d+); tunnels? leads? to valves?\s+([\s\S]+)$/);
    return {
        name: vMatch[1],
        rate: +vMatch[2],
        to: vMatch[3].split(',').map(n => n.trim()).sort(),
        pathmap: []
    };
}).sort((a, b) => a.name < b.name ? -1 : 1);
// add shortest path maps (strip pathmaps of valves which are not the start valve and have rate 0)
valves.forEach(v => v.pathmap = shortestPathMap(v.name).filter(p => p.name === start || p.rate > 0));
// only keep valves which are start or have rate > 0
valves = valves.filter(v => v.name === start || v.rate > 0);
// save some stuff to look at
writeFile('valves_sorted.json', stringify(valves));
// permutator
var iteration = 0;
var maxScore = getMaxWithRemaining(start, valves.map(v => v.name).filter(v => v != start), minutes, 0, part === 2)[0];
console.log(stringify(maxScore));
//# sourceMappingURL=day16.js.map