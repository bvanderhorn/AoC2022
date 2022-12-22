import * as fs from "fs";
type Valve = {
    name: string,
    rate: number,
    to: string[]
}
function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

// parse
const input: string = fs.readFileSync('valves.txt', 'utf8');
const valves: Valve[] = input.split('\r\n').map(v => {
    var vMatch = v.match(/Valve\s+(\w+)\s+has flow rate=(\d+); tunnels? leads? to valves?\s+([\s\S]+)$/);
    return {
        name: vMatch[1],
        rate: +vMatch[2],
        to: vMatch[3].split(',').map(n => n.trim())
    }
});
console.log(stringify(valves));