function sum($array){
    $sum = 0; 
    $array | % {$sum += $_}
    return $sum
}
function toNum($rounds){
    $replace = 'ABCXYZ'
    $with = '123123'
    [int32[][]]$out = @()
    foreach($round in $rounds){
        for ($i=0; $i -lt $replace.length; $i++){
            $round = $round -replace $replace.substring($i,1), $with.substring($i,1)
        }
        $out += ,($round.split(' ') | % {[int] $_})
    }
    
    return $out
}

function getPoints($nums){
    $mod = ($nums[1] - $nums[0] + 3) % 3
    $points = $nums[1]
    if ($mod -eq 0){
        $points += 3
    }
    elseif ($mod -eq 1){
        $points += 6
    }

    return $points
}

$guide = Get-Content guide.txt
$rounds = toNum($guide)
$points1  = $rounds | % {getPoints($_)}
sum($points1)

function updateRound($round) {
    $opp = $round[0]
    $me = 0
    if ($round[1] -eq 1){
        $me = $opp -1
    } elseif ($round[1] -eq 2){
        $me = $opp
    } elseif ($round[1] -eq 3){
        $me = $opp + 1
    }

    if ($me -eq 0){
        $me = 3
    } elseif ($me -gt 3){
        $me = $me - 3
    }

    return @($opp, $me)
}

$rounds2 = @()
foreach ($round in $rounds) {
    $rounds2 += ,(updateRound($round))
}

$points2  = $rounds2 | % {getPoints($_)}
sum($points2)






