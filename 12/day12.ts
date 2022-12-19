import * as fs from "fs";
function isReachable(fromPos: number[], toPos: number[]) : boolean {
    return map[toPos[0]][toPos[1]] - map[fromPos[0]][fromPos[1]] > -2;
}
function getNeighbours(pos:number[]): number[][] {
    let neighbours : number[][] = [];
    let nb = [
        [pos[0]-1, pos[1]],
        [pos[0]+1, pos[1]],
        [pos[0], pos[1]-1],
        [pos[0], pos[1]+1]
    ];
    for (const n of nb){
        if (n[0] >= 0 && n[0]<xLength && n[1]>=0 && n[1]<yLength && isReachable(pos,n)) neighbours.push(n); 
    }
    return neighbours;
}

function isAlreadyVisited(pos:number[]) : boolean {
    return visited.filter(el => el[0]=== pos[0] && el[1] === pos[1]).length === 1;
}

function getNearestUnvisited() : number[] {
    let nearest: number[] = [];
    let minDist: number = inf;
    for (let i=0;i<xLength;i++){
        for (let j=0;j<yLength;j++){
            if (!isAlreadyVisited([i,j]) && dist[i][j] < minDist) {
                nearest = [i,j];
                minDist = dist[i][j];
            }
        }
    }
    return nearest;
}

// params
const startPos = [20,0];
const endPos = [20,40];
const inf: number = 10000000000;

// parse
const input: string = fs.readFileSync('map.txt', 'utf8');
const map = input.split('\r\n').map(el => el.split('').map(s => s.charCodeAt(0) - 97));
const xLength = map.length;
const yLength = map[0].length;
var dist: number[][] = [];
for (let i=0; i<xLength;i++) dist.push(Array(yLength).fill(inf));
map[startPos[0]][startPos[1]] = 0;
map[endPos[0]][endPos[1]] = 25;
// dist[startPos[0]][startPos[1]] = 0;
dist[endPos[0]][endPos[1]] = 0;
console.log(startPos);
fs.writeFileSync('startDist.txt',dist.map(el => el.join(',')).join('\r\n'));

// Dijkstra over all coordinates
var visited: number[][] = [];
for (let i=0;i<xLength*yLength;i++){
    let current = getNearestUnvisited();
    //if (current.toString() === endPos.toString()) break;
    for (const n of getNeighbours(current)){
        let curDist = dist[n[0]][n[1]];
        let newDist = dist[current[0]][current[1]] + 1;
        if (curDist > newDist) dist[n[0]][n[1]] = newDist;
    }
    visited.push(current);
    if (i%yLength === 0) console.log( (i/yLength/xLength*100).toPrecision(2) + "% done" );
}

fs.writeFileSync('dist.txt',dist.map(el => el.join(',')).join('\r\n'));
console.log(" Distance from original starting point: " + dist[startPos[0]][startPos[1]]);

// part 2
let minADist = dist.map((el,x) => el.filter((d,y) => map[x][y] === 0).sort((a,b) => a > b ? 1: -1)[0]).sort((a,b) => a > b ? 1: -1)[0];
console.log(" minimal A distance : " + minADist);
