import * as fs from "fs";
function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

// parse
const input: string = fs.readFileSync('valves.txt', 'utf8');
const valves = input.split('\r\n');
console.log(valves.slice(0,5));