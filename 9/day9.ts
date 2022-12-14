import { equal } from "assert";
import * as fs from "fs";

function uniqueArray(array: number[][]) {
    return Array.from(
        new Map(array.map((p) => [JSON.stringify(p), p])).values()
      )
}

function equals(first: any[], second: any[]) : boolean {
    return JSON.stringify(first) === JSON.stringify(second);
}
function newTailPos(headPos: number[], oldTailPos: number[]) : number[] {
    var diff = headPos.map((el, index) => el - tailTrail[tailTrail.length-1][index]);
    if (Math.abs(diff[0]) == 2) {
        return [headPos[0] - (diff[0]/2) , headPos[1]];
        //console.log(" tail: " + tailTrail[tailTrail.length -1].toString());
    } else if (Math.abs(diff[1]) == 2) {
       return [headPos[0] , headPos[1] - (diff[1]/2)];
        //console.log(" tail: " + tailTrail[tailTrail.length -1].toString());
    } else {
        return oldTailPos;
    }
}

const input: string = fs.readFileSync('motions.txt', 'utf8');
// console.log(input);
const motions = input.split('\r\n').map(el => el.split(' ')).map(el => [el[0], +el[1]]);
console.log(motions.slice(0,10));
var tailTrail : number[][] = [[0,0]];
var headPos : number[] = [0,0];
for (var motion of motions){
    for (let i=0;i<motion[1];i++){
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
        //console.log("head: " + headPos.toString());
        var oldTailPos = tailTrail[tailTrail.length-1];
        var tailPos = newTailPos(headPos, oldTailPos);
        if (!equals(oldTailPos, tailPos)){
            tailTrail.push(tailPos);
        }
    }
}
console.log(tailTrail.slice(0,15));
console.log(uniqueArray(tailTrail.slice(0,15)));
console.log(uniqueArray(tailTrail).length);
