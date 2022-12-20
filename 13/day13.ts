import * as fs from "fs";

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

function getNextBlock(str:string) : string {
    let ls = 0;
    let rs = 0;  
    for (var i=0;i<str.length;i++){
        let cur = str.slice(i,i+1);
        if (cur===l) ls++;
        if (cur===r) rs++;
        if (ls == rs && cur === sep) return str.slice(0,i);;
    }
    
    return str;
}

function splitInBlocks(str:string) : string[] {
    let rem = str;
    var out : string[] = [];
    while (rem.length > 0){
        let nextBlock = getNextBlock(rem);
        out.push(nextBlock);
        rem = rem.slice(nextBlock.length+1,rem.length);
    }
    return out;
}

function parse(str:string) : any {
    if (str.slice(0,1) === l) {
        var out = [];
        var elements = splitInBlocks(str.slice(1,str.length -1));
        for (const el of elements) out.push(parse(el));
        return out;
    } else {
        return +str;
    }
}

function isOrderCorrect(pair: any[]) : string {
    let left: any = pair[0];
    let right: any = pair[1];

    for (let i=0;i<left.length;i++) {
        if (i >= right.length) return 'false';
        if (typeof(left[i]) === 'number' && typeof(right[i]) === 'number') {
            if (left[i] === right[i]) continue;
            return (left[i] < right[i]).toString();
        }
        let leftI: any = typeof(left[i]) === 'number' ? [left[i]] : left[i];
        let rightI: any = typeof(right[i]) === 'number' ? [right[i]] : right[i];
        let sub = isOrderCorrect([leftI, rightI]);
        if (sub != 'equal') return sub;
    }
    if (left.length < right.length) return 'true';
    return 'equal';
}

// params
const l = '[';
const r = ']';
const sep = ',';

// parse
const input: string = fs.readFileSync('packets.txt', 'utf8');
const pairs = input.split('\r\n\r\n').map(el => el.split('\r\n'));
console.log(pairs.slice(0,3));
console.log(stringify(parse(pairs[0][0])));

// compare
var count = 0;
for (let i=0;i<pairs.length;i++){
    let left = parse(pairs[i][0]);
    let right = parse(pairs[i][1]);
    let isCorrect = isOrderCorrect([left,right]);
    console.log(" pair " + i + ": " + isCorrect);
    if (isCorrect != 'false') count += i +1;
}
console.log(count);
