using System.Text.RegularExpressions;
// See https://aka.ms/new-console-template for more information
List<string> NewSplit(string input, string separator)
{
    return input.Split(new string[] { separator }, StringSplitOptions.None).ToList();
}

void WriteList(List<string> input, string separator = "\r\n") 
{
    Console.WriteLine(input.Aggregate((a, b) => a + separator + b));
}

void WriteStacks(List<List<string>> stacks)
{
    foreach (var stack in stacks) {
        WriteList(stack, ", ");
    }
}

void WriteEndString(List<List<string>> stacks)
{
    var endstring = "";
    foreach (var stack in stacks) {
        endstring += stack.Last();
    }
    Console.WriteLine(endstring);
}

List<List<string>> ReadStacks(string rawStacks) 
{
    var lines = NewSplit(rawStacks, "\r\n");
    lines.RemoveAt(lines.Count()-1);
    var nofStacks = NewSplit(lines.Last(), " ").Count();

    var stacks = new List<List<string>>();
    // preallocate
    for (var j=0; j< nofStacks; j++)
    {
        stacks.Add(new List<string>());
    }

    // build stacks
    for (var i = lines.Count() -1; i >= 0; i--)
    {
        for (var j=0; j< nofStacks; j++)
        {
            var letter = lines[i].Substring(j*4 + 1, 1);
            if (letter != " "){
                stacks[j].Add(letter);
            }
        }
    }

    return stacks;
}

List<List<string>> ApplyMoves(List<List<string>> stacks, List<string> moves, bool reverse = true)
{
    var outStacks = stacks;
    foreach (var move in moves) 
    {
        // Console.WriteLine(move);
        var amount = Int32.Parse(Regex.Replace(Regex.Replace(move, "^move ", "")," [\\s\\S]*$",""));
        var from = Int32.Parse(Regex.Replace(Regex.Replace(move, "^[\\s\\S]*from ", "")," [\\s\\S]*$","")) -1;
        var to = Int32.Parse(Regex.Replace(Regex.Replace(move, "^[\\s\\S]*to ", ""),"\\s*$","")) -1;

        var moveLetters = outStacks[from].GetRange(outStacks[from].Count() - amount, amount);
        if (reverse)
        {
            moveLetters.Reverse();
        }
        outStacks[from] = outStacks[from].GetRange(0, outStacks[from].Count() - amount);
        outStacks[to].AddRange(moveLetters);
    }
    return outStacks;
}

var input = System.IO.File.ReadAllText(@"input.txt");
var StacksMoves = NewSplit(input, "\r\n\r\n");
var stacks = ReadStacks(StacksMoves[0]);
Console.WriteLine(StacksMoves[0]);
foreach (var stack in stacks) {
    WriteList(stack, ", ");
}

var moves = NewSplit(StacksMoves[1],"\r\n");
// WriteList(moves.GetRange(0,10));
var m = Regex.Match("move 1 from 8 to 24",@"move (\d+) from (\d+) to (\d+)");
// Console.WriteLine(m.Value);
var move = "move 25 from 8 to 24";
var amount = Int32.Parse(Regex.Replace(Regex.Replace(move, "^move ", "")," [\\s\\S]*$",""));
var from = Int32.Parse(Regex.Replace(Regex.Replace(move, "^[\\s\\S]*from ", "")," [\\s\\S]*$",""));
var to = Int32.Parse(Regex.Replace(Regex.Replace(move, "^[\\s\\S]*to ", ""),"\\s*$",""));
// Console.WriteLine(amount + ", " + from + ", " + to);

// part one
// var newStacks = ApplyMoves(stacks, moves);
// WriteStacks(newStacks);
// WriteEndString(newStacks);

// part two
var stacks2 = ApplyMoves(stacks, moves, false);
WriteStacks(stacks2);
WriteEndString(stacks2);