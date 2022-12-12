function sum($array){
    $sum = 0; 
    $array | % {$sum += $_}
    return $sum
}

$energy = Get-Content energy.txt
$elves = ($energy -join "\r\n").split("\r\n\r\n") 
$elvesEnergy = $elves | % {sum($_.split("\r\n"))} | Sort-Object -desc

$elvesEnergy[0]
sum($elvesEnergy[0..2])

