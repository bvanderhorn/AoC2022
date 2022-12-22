"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
// parse
const input = fs.readFileSync('valves.txt', 'utf8');
const valves = input.split('\r\n');
console.log(valves.slice(0, 5));
//# sourceMappingURL=day16.js.map