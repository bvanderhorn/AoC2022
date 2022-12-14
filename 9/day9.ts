import { equal } from "assert";
import * as fs from "fs";

function uniqueArray(array: number[][]) {
    return Array.from(
        new Map(array.map((p) => [JSON.stringify(p), p])).values()
      )
}

function log(test:boolean, print:any) {
    if (test) console.log(print);
}

function equals(first: any[], second: any[]) : boolean {
    return JSON.stringify(first) === JSON.stringify(second);
}
function newTailPos(headPos: number[], oldTailPos: number[]) : number[] {
    var diff = headPos.map((el, index) => el - oldTailPos[index]);
    var xDiff = Math.abs(diff[0]);
    var yDiff = Math.abs(diff[1]);
    if (xDiff == 2 && yDiff == 2)   return [headPos[0] - (diff[0]/2) , headPos[1] - (diff[1]/2)];
    else if (xDiff == 2)            return [headPos[0] - (diff[0]/2) , headPos[1]];
    else if (yDiff == 2)            return [headPos[0] , headPos[1] - (diff[1]/2)];
    else                            return oldTailPos;
}

var test = false;
const input: string = fs.readFileSync('motions.txt', 'utf8');
// console.log(input);
var motions = input.split('\r\n').map(el => el.split(' ')).map(el => [el[0], +el[1]]);
// motions = motions.slice(1420,1430);
console.log(motions.slice(0,10));
var knots = 10;
var tailTrail : number[][] = [[0,0]];
var headPos : number[] = [0,0];
var rope: number[][] = [];
for (var i=0;i<knots;i++) rope.push([0,0]);
for (var motion of motions){
    log(test, "motion: " + motion.toString());
    for (let i=0;i<motion[1];i++){
        // move the head
        switch (motion[0]){
            case 'R':
                headPos[0]++;
                break;
            case 'L':
                headPos[0]--;
                break;
            case 'U':
                headPos[1]++;
                break;
            case 'D':
                headPos[1]--;
                break;
        }
        log(test, " head: " + headPos.toString());
        rope[0] = headPos;

        // move all individual knots
        for (var j=1; j<rope.length; j++){
            rope[j] = newTailPos(rope[j-1], rope[j]);
            log(test,"  knot " + j + ": " + rope[j].toString());
        }

        // add last knot position to tail trail if new
        if (!equals(tailTrail[tailTrail.length-1], rope[rope.length-1])){
            tailTrail.push(rope[rope.length-1]);
            log(test," tail: " + tailTrail[tailTrail.length -1].toString());
        }
    }
}
console.log(tailTrail.slice(0,20));
console.log(uniqueArray(tailTrail.slice(0,20)));
console.log(uniqueArray(tailTrail).length);
