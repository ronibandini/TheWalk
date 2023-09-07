<?php

// The Walk
// Roni Bandini, September 2023
// MIT license
// @RoniBandini bandini.medium.com
// Read coordinates from CSV file and present map with The Walk location
// http://maps.google.com/maps?q=-34.6037,-58.3816&z=17

$GoogleMapsApiKey="000000";

$lines = file('coordinates.csv');
$count = 0;
foreach($lines as $line) {
    $count += 1;
    $lineArray=explode(",", $line);
}

$lat=$lineArray[0];
$lng=$lineArray[1];
?>
<img src="images/thewalk.png" alt="The Walk">
<br>
<p>The Walk is currently at: <?=$lat?>,<?=$lng?></p>
<br>
<div style="text-decoration:none; overflow:hidden;max-width:100%;width:800px;height:800px;">
  <div id="gmap-canvas" style="height:100%; width:100%;max-width:100%;">
    <iframe style="height:100%;width:100%;border:0;" frameborder="0" src="https://www.google.com/maps/embed/v1/place?q=<?=$lat?>,<?=$lng?>&key=<?=$GoogleMapsApiKey?>">
    </iframe></div>
    <style>#gmap-canvas img.text-marker{max-width:none!important;background:none!important;}img{max-width:none}
    </style>
  </div>

  <p><a href="https://bandini.medium.com/the-walk-la-m%C3%A1quina-de-caminar-mapas-4cd75a607f29">The Walk</a> Roni Bandini, September 2023</p>
