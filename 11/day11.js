"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
function log(test, print) {
    if (test)
        console.log(print);
}
function stringify(object) {
    return JSON.stringify(object, null, 4);
}
function isDivisible(num, div) {
    return num / div === Math.floor(num / div);
}
const test = true;
// parse input
const input = fs.readFileSync('monkey_instructions.txt', 'utf8');
const instructions = input.split('\r\n\r\n').map(el => el.split('\r\n'));
//console.log(instructions);
var monkeys = [];
instructions.forEach(instruction => {
    var monkey = {
        items: [],
        operation: null,
        inspections: 0,
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
        if (itemsMatch != null)
            monkey.items = itemsMatch[1].split(',').map(el => +(el.trim()));
        else if (operationMatch != null)
            monkey.operation = operationMatch[1].trim().replace('new', 'newer');
        else if (divisibleMatch != null)
            monkey.evaluation.divisible = +divisibleMatch[1].trim();
        else if (ifTrueMatch != null)
            monkey.evaluation.trueMonkey = +ifTrueMatch[1].trim();
        else if (ifFalseMatch != null)
            monkey.evaluation.falseMonkey = +ifFalseMatch[1].trim();
    }
    monkeys.push(monkey);
    //log(test, stringify(monkey));
});
log(test, stringify(monkeys));
// execute
const maxDiv = monkeys.map(m => m.evaluation.divisible).reduce((a, b) => a * b);
const rounds = 10000;
for (var i = 0; i < rounds; i++) {
    //log(test, "Round " + (i+1));
    for (var j = 0; j < monkeys.length; j++) {
        var m = monkeys[j];
        m.items.map(old => {
            var newer = 0;
            eval(m.operation);
            newer = newer % maxDiv;
            //log(test," operation: (old = " + old + ") -> " + m.operation + " -> newer = " + newer + " -> return " + Math.floor(newer/3.));
            //return Math.floor(newer/3.);
            return newer;
        }).forEach(item => {
            //log(test, "  item: "+item + ", divisible: " + m.evaluation.divisible + ", isDivisible: " + (div === Math.floor(div)).toString());
            monkeys[isDivisible(item, m.evaluation.divisible) ? m.evaluation.trueMonkey : m.evaluation.falseMonkey].items.push(item);
        });
        monkeys[j].inspections += monkeys[j].items.length;
        monkeys[j].items = [];
    }
    //log(test, "Items:");
    //monkeys.forEach((monkey,index) => log(test, " Monkey " + index + ": " + monkey.items.join(", ")));
}
log(test, "Inspections: ");
monkeys.forEach((monkey, index) => log(test, " Monkey " + index + ": " + monkey.inspections));
var sum = monkeys.map(el => el.inspections).sort((a, b) => b - a).slice(0, 2);
log(test, "Monkey business: " + [sum[0] * sum[1]]);
//log(test, maxDiv.toString());
//# sourceMappingURL=day11.js.map