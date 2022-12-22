"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
// parse
const input = fs.readFileSync('valves.txt', 'utf8');
const valves = input.split('\r\n').map(v => {
    var vMatch = v.match(/Valve\s+(\w+)\s+has flow rate=(\d+); tunnels? leads? to valves?\s+([\s\S]+)$/);
    return {
        name: vMatch[1],
        rate: +vMatch[2],
        to: vMatch[3].split(',').map(n => n.trim())
    };
});
console.log(stringify(valves));
//# sourceMappingURL=day16.js.map