import * as fs from "fs";

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

// parse
const input: string = fs.readFileSync('traces.txt', 'utf8');
const traces = input.split('\r\n');
console.log(traces.slice(0,10));