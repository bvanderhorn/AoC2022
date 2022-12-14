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
var emptyMonkey = {
    items: [],
    operation: null,
    inspections: 0,
    evaluation: {
        divisible: null,
        trueMonkey: null,
        falseMonkey: null
    }
};
const test = true;
// parse input
const input = fs.readFileSync('monkey_instructions.txt', 'utf8');
const instructions = input.split('\r\n\r\n').map(el => el.split('\r\n'));
//console.log(instructions);
var monkeys = [];
instructions.forEach(instruction => {
    var monkey = emptyMonkey;
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
    monkeys.push({
        items: monkey.items,
        operation: monkey.operation,
        inspections: 0,
        evaluation: {
            divisible: monkey.evaluation.divisible,
            trueMonkey: monkey.evaluation.trueMonkey,
            falseMonkey: monkey.evaluation.falseMonkey
        }
    });
    //log(test, stringify(monkey));
});
log(test, stringify(monkeys));
// execute
const rounds = 20;
for (var i = 0; i < rounds; i++) {
    log(test, "Round " + (i + 1));
    for (var j = 0; j < monkeys.length; j++) {
        var m = monkeys[j];
        m.items.map(old => {
            var newer = 0;
            eval(m.operation);
            //log(test," operation: (old = " + old + ") -> " + m.operation + " -> newer = " + newer + " -> return " + Math.floor(newer/3.));
            return Math.floor(newer / 3.);
        }).forEach(item => {
            //log(test, "  item: "+item + ", divisible: " + m.evaluation.divisible + ", isDivisible: " + (div === Math.floor(div)).toString());
            var div = item / m.evaluation.divisible;
            monkeys[(div === Math.floor(div)) ? m.evaluation.trueMonkey : m.evaluation.falseMonkey].items.push(item);
        });
        monkeys[j].inspections += monkeys[j].items.length;
        monkeys[j].items = [];
    }
    log(test, "Items:");
    monkeys.forEach((monkey, index) => log(test, " Monkey " + index + ": " + monkey.items.join(", ")));
}
log(test, "Inspections: ");
monkeys.forEach((monkey, index) => log(test, " Monkey " + index + ": " + monkey.inspections));
var sum = monkeys.map(el => el.inspections).sort((a, b) => b - a).slice(0, 2);
log(test, "Monkey business: " + [sum[0] * sum[1]]);
//# sourceMappingURL=day11.js.map