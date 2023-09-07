<?php

// The Walk
// Roni Bandini, September 2023
// MIT license
// @RoniBandini bandini.medium.com
// receives coordinates from The Walk Python and updates local csv file

// http://comersus.com/thewalk/coordinates.php?lat=-34.6037&lng=-58.3816

$lat	=$_GET['lat'];
$lng	=$_GET['lng'];

$lat	=filter_var($lat, FILTER_SANITIZE_STRING);
$lng	=filter_var($lng, FILTER_SANITIZE_STRING);

$lat  = substr($lat, 0, 30);
$lng  = substr($lng, 0, 30);

$myfile = fopen("coordinates.csv", "w") or die("Unable to open file!");
$txt = $lat.",".$lng."\n";
fwrite($myfile, $txt);
fclose($myfile);

echo "The Walk coordinates set to: ".$lat.",".$lng
?>
