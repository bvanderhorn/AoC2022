"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
// parse
const input = fs.readFileSync('traces.txt', 'utf8');
const traces = input.split('\r\n');
console.log(traces.slice(0, 10));
//# sourceMappingURL=day14.js.map