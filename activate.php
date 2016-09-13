<?php
// we'll generate XML output
header('Content-Type: text/xml');
// generate XML header
echo '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
// create the <response> element
echo '<response>';
// retrieve the user name
$cmd = $_GET['gpio'];
$output = shell_exec ( $cmd );
echo "<pre>$output</pre>";
// close the <response> element
echo '</response>';
?>