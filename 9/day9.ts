import * as fs from "fs";
const input: string = fs.readFileSync('motions.txt', 'utf8');
// console.log(input);
const motions = input.split('\r\n').map(el => el.split(' ')).map(el => [el[0], +el[1]]);
console.log(motions.slice(1610,1630));