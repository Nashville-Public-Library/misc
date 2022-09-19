
<?php

/*
Print all fields from TL Icecast server.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
*/

$source = "http://npl.streamguys1.com/status.xsl";

$dom = new DOMDocument();
$dom->loadHTMLFile($source);
$tag = $dom->getElementsByTagName('tr');
foreach ($tag as $lala) {
    echo $lala->nodeValue, PHP_EOL;
}

?>
