const fs = require('fs');

function fullyContains(line){
  nums = line.match(/^(\d+)\-(\d+)\,(\d+)\-(\d+)$/).slice(1,5).map(el => +el);
  return (nums[0] <= nums[2] && nums[1] >= nums[3]) || (nums[2] <= nums[0] && nums[3] >= nums[1])
}

function partiallyOverlap(line) {
  nums = line.match(/^(\d+)\-(\d+)\,(\d+)\-(\d+)$/).slice(1,5).map(el => +el);
  return (nums[1] >= nums[2] && nums[0] <= nums[3])
}

input = fs.readFileSync('pairs.txt', 'utf8');
lines = input.split('\r\n');
console.log(lines.slice(0,10));
console.log(lines.map(el => fullyContains(el)*1).reduce((a, b) => a + b, 0));
console.log(lines.map(el => partiallyOverlap(el)*1).reduce((a, b) => a + b, 0));
  