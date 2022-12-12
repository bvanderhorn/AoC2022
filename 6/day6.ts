import * as fs from "fs";

const input: string = fs.readFileSync('input.txt', 'utf8');
// console.log(input);
const inputArray = input.split('');
const packageLength: number = 14;
const packageIndices = inputArray.map((el, index) => {
    const sub = inputArray.slice(index-(packageLength-1), index+1);
    return (index >= (packageLength -1) && sub.length === [...new Set(sub)].length) ? index : 0 ;
}).filter(el => el > 0);
console.log(packageIndices[0]+ 1);