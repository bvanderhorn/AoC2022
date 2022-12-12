function splitCompartments($rucksack) {
    $size = $rucksack.length/2 
    return @(
        $rucksack.substring(0, $size),
        $rucksack.substring($size)
    )
}

function bothContainCharacter($strings){
    for ($i=0; $i -lt $strings[0].length; $i++){
        if ($strings[1].Contains($strings[0].substring($i,1))){
             return $strings[0].substring($i,1)
        }
    }
}

function allThreeContainChar($array){
    $letters = 'abcdefghijklmnopqrstuvwxyz'
    $letters += $letters.ToUpper()
    for ($i=0; $i -lt $letters.length; $i++){
        $char = $letters.substring($i,1)
        if ($array[0].Contains($char) -and $array[1].Contains($char) -and $array[2].Contains($char)) {
            return $char
        }
    }
}

$rucksacks = Get-Content rucksacks.txt
# $compartments = convertArray -array $rucksacks -func $function:splitCompartments
$compartments = @()
$rucksacks | % {$compartments += ,(splitCompartments($_))}
$prios = @()
$compartments | % { $prios += (bothContainCharacter $_) }

$prioValues = 'abcdefghijklmnopqrstuvwxyz'
$prioValues += $prioValues.ToUpper()
$sum = 0;
$prios | % { $sum += 1 + $prioValues.indexOf($_)}
$sum

$sum2 = 0;
for ($i = 0; $i -lt ($rucksacks.length/3); $i++) {
    $min = $i * 3
    $max = $min + 2
    $char = allThreeContainChar($rucksacks[$min..$max])
    $sum2 += 1 + $prioValues.IndexOf($char)
}
$sum2