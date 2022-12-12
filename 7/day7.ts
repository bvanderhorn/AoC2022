// npm install --save-dev typescript @types/node fs
// Ctrl + Shift + B -> watch
// >> node day7.js

import { dir } from "console";
import * as fs from "fs";

enum Type {
    dir,
    file
}
type Element = {
    name: string,
    type: Type,
    parent: string,
    level: number,
    size: number,
    children: Element[]
}

function fullName(parent: string, shortName: string) : string {
    return parent + (parent === '/' ? '' : '/') + shortName;
}

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

function getParent(element: Element, elements: Element[]) : Element {
    return elements.filter(el => el.name === element.parent)[0];
}

function sumSize(elements: Element[]) : number {
    return elements.map(el => el.size).reduce((a,b) => a+b, 0);
}

const input: string = fs.readFileSync('input.txt', 'utf8');
// console.log(input.slice(0,1000));
const commands : string[] = input.split('\r\n$');
// console.log(commands.slice(0,10));
const commandsSplit: string[][] = commands.map(el => el.split('\r\n'));
console.log(commandsSplit.slice(0,10));


let elements : Element[] = [];
elements.push({
    name: "/",
    type: Type.dir,
    parent: '',
    level: 0,
    size: null,
    children: []
});

var current: Element = elements[0];
var next = "";
var iteration = 0;
var maxLevel = 0;
for (const comm of commandsSplit){
    //console.log(iteration++);

    var cdMatch = comm[0].match(/cd\s+(\S+)/);
    var lsMatch = comm[0].match(/^\s*ls\s*$/);
    if (cdMatch != null){
        var cd = cdMatch[1];
        
        if (cd === ".."){
            next = current.parent;
        } else if (cd == "/") {
            next = cd;
        } else {
            next = fullName(current.name,cd);
        }
        //console.log(" to " + next);
        current = elements.filter(el => el.name == next)[0];
    } else if (lsMatch != null) {
        if (comm.length > 1 && (current.level + 1) > maxLevel) {
            maxLevel = current.level + 1;
        }
        for (const element of comm.slice(1)){
            var dirMatch = element.match(/^\s*dir\s+(\S+)\s*$/);
            var fileMatch = element.match(/^\s*(\d+)\s+(\S+)\s*$/);
            var fn = "";
            if (dirMatch != null){
                fn = fullName(current.name, dirMatch[1]);
                if (elements.filter(el => el.name === fn).length === 0){
                    elements.push({
                        name: fn,
                        type: Type.dir,
                        parent: current.name,
                        level: current.level + 1,
                        size: null,
                        children: []
                    });
                }
            } else if (fileMatch != null) {
                fn = fullName(current.name, fileMatch[2]);
                if (elements.filter(el => el.name === fn).length === 0){
                    elements.push({
                        name: fn,
                        type: Type.file,
                        parent: current.name,
                        level: current.level + 1,
                        size: +fileMatch[1],
                        children: []
                    });
                }
            }
        }
    }
}

for (let i = maxLevel -1; i>=0; i--){
    var dirsOnLevel = elements.filter(el => el.level === i && el.type == Type.dir);
    for (const dirOnLevel of dirsOnLevel){
        var index = elements.findIndex(el => el.name === dirOnLevel.name);
        elements[index].size = sumSize(elements.filter(el => el.parent === dirOnLevel.name));
        elements[index].children = elements.filter(el => el.parent === elements[index].name);
    }
}
var lim = 100000;
// var limitedElements = elements.filter(el => el.size <= lim && getParent(el, elements).size > lim && el.type == Type.dir);
var limitedElements = elements.filter(el => el.size <= lim && el.type == Type.dir);
// console.log(limitedElements);
console.log(sumSize(limitedElements));
// fs.writeFileSync('./elements.json',stringify(elements[0]), {encoding:'utf8',flag:'w'});
// fs.writeFileSync('./limitedElements.json',stringify(limitedElements), {encoding:'utf8',flag:'w'});
var systemSize = 70000000;
var neededSize = 30000000;
var usedSize = elements.filter(el => el.name === '/')[0].size;
var availableSize = systemSize - usedSize;
var neededExtra = neededSize - availableSize;
console.log("needed extra: " + neededExtra);
var smallestFittingDir = elements.filter(el => el.type === Type.dir && el.size >= neededExtra).sort((a, b) => (a.size > b.size) ? 1 : -1)[0];
console.log(smallestFittingDir);



