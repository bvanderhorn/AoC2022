import * as fs from "fs";
const input: string = fs.readFileSync('trees.txt', 'utf8');
console.log(input);
const lines = input.split('\r\n').map(el => el.split('').map(e => +e));
// console.log(lines);

function max(array: number[]) : number {
    return (array.length === 0) ? 0 : Math.max(...array);
}



function visible(row: number, col:number) : boolean {
    var left : number[] = col === 0 ? [] : lines[row].slice(0,col);
    var right : number[] = col === (lines[row].length -1) ? [] : lines[row].slice(col + 1);
    
    var up : number[] = [];
    if (row != 0) for (const line of lines.slice(0,row)) up.push(line[col]);

    var down: number[] = [];
    if (row != lines.length -1) for (const line of lines.slice(row+1)) down.push(line[col]);

    return lines[row][col] > Math.min(...[max(left), max(right), max(up), max(down)]);
};

var nofVisible = 0;
for (let i=0; i<lines.length;i++){
    for (let j=0;j<lines[0].length;j++){
        if(visible(i,j)) nofVisible++;
    }
}

console.log(nofVisible);