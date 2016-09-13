<?php
// we'll generate XML output
header('Content-Type: text/xml');
// generate XML header
echo '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
// create the <response> element
// retrieve gpio, action and value
echo '<response>';
$gpio = $_GET['gpio'];
$action = $_GET['action'];
$value = $_GET['value'];
echo $action . $gpio . $value;
// setup the command
$cmd = "gpio ";
$cmd .= $action;
$cmd .= " ";
$cmd .= $gpio;
$cmd .= " ";
$cmd .= $value;
$output = shell_exec ( $cmd );
echo "<pre>".$cmd."
Response: ".$output."</pre>";
// close the <response> element
echo '</response>';

function my($a)
{
	echo "$a\n";
}
?>
