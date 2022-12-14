import * as fs from "fs";

type Evaluation = {
    divisible: number,
    trueMonkey: number,
    falseMonkey: number
}
type Monkey = {
    items: number[],
    operation: string,
    evaluation: Evaluation
}
function log(test:boolean, print:any) {
    if (test) console.log(print);
}

function stringify(object: any) : string {
    return JSON.stringify(object, null, 4);
}

const test = true;
const input: string = fs.readFileSync('monkey_instructions.txt', 'utf8');
const instructions = input.split('\r\n\r\n').map(el => el.split('\r\n'));
console.log(instructions);
var monkeys: Monkey[] = [];
instructions.forEach(instruction => {
    var monkey: Monkey =  {
        items: [],
        operation: null,
        evaluation: {
            divisible: null,
            trueMonkey: null,
            falseMonkey: null
        }
    };
    for (const line of instruction) {
        var itemsMatch = line.match(/^\s+Starting\s+items:\s+([\s\S]+)\s*$/);
        var operationMatch = line.match(/^\s+Operation:\s+([\s\S]+)\s*$/);
        var divisibleMatch = line.match(/^[\s\S]*divisible\s+by\s+(\d+)\s*$/);
        var ifTrueMatch = line.match(/^\s*If\s+true:\D+(\d+)\s*$/);
        var ifFalseMatch = line.match(/^\s*If\s+false:\D+(\d+)\s*$/);

        if      (itemsMatch != null)        monkey.items = itemsMatch[1].split(',').map(el => +(el.trim()));
        else if (operationMatch != null)    monkey.operation = operationMatch[1].trim();
        else if (divisibleMatch != null)    monkey.evaluation.divisible = +divisibleMatch[1].trim();
        else if (ifTrueMatch != null)       monkey.evaluation.trueMonkey = +ifTrueMatch[1].trim();
        else if (ifFalseMatch != null)      monkey.evaluation.falseMonkey = +ifFalseMatch[1].trim();
    }
    monkeys.push(monkey);
});

log(test, stringify(monkeys));
