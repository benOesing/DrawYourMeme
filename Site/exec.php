<?php
function call(){
$arg1 = $_GET['a1']; // Extra
$arg2 = $_GET['a2']; // Border = 1, no border = 0
$arg3 = $_GET['a3']; // Style
$arg4 = $_GET['a4']; // FPS
$arg5 = $_GET['a5']; // Duration
$arg6 = $_GET['a6']; // BlackThreshold
$arg7 = $_GET['a7']; // Name
$arg7_new = preg_replace('/_.*/','',$arg7);
$arg7_folder = preg_replace('/[^A-Za-z0-9_]/','',$arg7);

//Check
$parseError = "";
$run = 1;

if($run == 1 && file_exists("/srv/users/maximeme/apps/drawyourmeme/public/Dankmemes/" . $arg7_folder . ".gif")){
	$run = 0;
	$parseError .= "File already exists";
}

if($run == 1 && !preg_match("/^([0-9]|[1-9][0-9]|[1-9][0-9][0-9])$/",$arg1)){
	$run = 0;
	$parseError .= "Bordersize " . $arg1 . " != [0,999] ";
}

if($run == 1 && !preg_match("/^[0-1]$/",$arg2)){
	$run = 0;
	$parseError .= "Border? " .$arg2 ." != [0,1] ";
}

if($run == 1 && !preg_match("/^[0-8]|9[0-4]$/",$arg3)){
	$run = 0;
	$parseError .= "Style " .$arg3 . " != [0..8,90,91,92,93,94] ";
}

if($run == 1 && !preg_match("/^([1-9]|[1-3][0-9])$/",$arg4)){
	$run = 0;
	$parseError .= "FPS " .$arg4 . " != [1,39] ";
}


if($run == 1 && !preg_match("/^([1-9]|[1-2][0-9])$/",$arg5)){
	$run = 0;
	$parseError .= "Duration " .$arg5 . " != [1,29] ";
}

if($run == 1 && !preg_match("/^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$/",$arg6)){
	$run = 0;
	$parseError .= "Blackthreshold " .$arg6 . " != [0,255] ";
}

if($run == 1 && !preg_match("/^.{20}$/",$arg7_new)){
	$run = 0;
	$parseError .= "Name " .$arg6 . " Length != 20";
}

//Run
if($run == 0){ // <--- Deactivated the program
exec("/srv/users/maximeme/apps/drawyourmeme/public/DyM/PyMeme.py " .escapeshellarg($arg1)." " .escapeshellarg($arg1)." " .escapeshellarg($arg2)." " .escapeshellarg($arg3)." " .escapeshellarg($arg4)." " .escapeshellarg($arg5)." " .escapeshellarg($arg6) ." /srv/users/maximeme/apps/drawyourmeme/public/Upload/" .escapeshellarg($arg7_new).".png /srv/users/maximeme/apps/drawyourmeme/public/DyM/SaveSpace/" .escapeshellarg($arg7)." 2>&1",$output);
} else{
$output = [];
}


//Write action to txt log
$log  = $arg1 ."," .$arg2 ."," .$arg3 ."," .$arg4."," .$arg5 ."," .$arg6 ."," ."$arg7.png" ."," ."$arg7/" ."|" .implode("|",$output)."|" .$parseError .PHP_EOL;
file_put_contents('./Logs/log_'.date("Y.n.j").'.txt',$log, FILE_APPEND);
}
call();
?>