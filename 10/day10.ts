import * as fs from "fs";

function log(test:boolean, print:any) {
    if (test) console.log(print);
}
function registerCycle() {
    x.push(xnow);
    cycle++;
}
function drawPixel(index: number, x:number) : string {
    const pixel = index%40;
    return ((pixel >= x-1) && (pixel <= x+1)) ? '#' : '.';
}

function draw(x:number[], lineLength:number) {
    for (let i=0; i< x.length; i+= lineLength){
        console.log(x.slice(i, i+lineLength).map((el,index)=> drawPixel(index,el)).join(''));
    }
}

const test = false;
const input: string = fs.readFileSync('instructions.txt', 'utf8');
// console.log(input);
const instructions = input.split('\r\n').map(el => el.split(' '));
console.log(instructions.slice(0,20));
const evaluateCycles: number[] = [20,60,100,140, 180,220];
const lineLength = 40;


var cycle = 1;
var x : number[] = [];
var xnow = 1;
for (const command of instructions){
    if (command[0] === 'addx') {
        registerCycle();
        registerCycle();
        xnow += +command[1];
    } else { // command[0] == 'noop'
        registerCycle();
    }
}
var evaluateX: number[] = x.filter((el, index) => evaluateCycles.includes(index+1));
var signalStrength: number[] = evaluateX.map((el, index) => el*evaluateCycles[index]);
var sumSignalStrength : number = signalStrength.reduce((a,b) => a+b, 0);
log(test,x.map((el,index) => " cycle " + (index+1) + ": " + el).join('\r\n'));
console.log(evaluateCycles);
console.log(evaluateX);
console.log(signalStrength);
console.log(sumSignalStrength);
draw(x,lineLength);