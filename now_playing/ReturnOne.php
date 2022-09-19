<?php

/*
Print Now Playing metadata from TL Icecast server.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
*/

$source = "http://npl.streamguys1.com/status.xsl";
$index = 21;

$dom = new DOMDocument();
$dom->loadHTMLFile($source);
$tag = $dom->getElementsByTagName('td');
$result = $tag->item($index)->nodeValue;

echo $result;

?>