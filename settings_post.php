
<?php
$g_link = false;
$senactprog_active = $_POST['senactprog_active'];
$senactsen_active = $_POST['senactsen_active'];
$sampletime = $_POST['sampletime'];

//$returnString = $senactprog_active.", ";
//$returnString = $returnString.$senactsen_active.", ";
//$returnString = $returnString.$sampletime;
//echo $returnString;
echo Update($senactprog_active,$senactsen_active,$sampletime);


function Update($senactprog_active,$senactsen_active,$sampletime)
{
	$conn = GetMyConnection();
	if($conn)
	{
			$sql = "UPDATE senact_cntrl SET senactprog_active=$senactprog_active,senactsen_active=$senactsen_active,sampletime=$sampletime";
      echo $sql;
		  $retval = mysql_query( $sql, $conn );
    echo "retval: ".$retval;
	}
	CleanUpDB();
  
  if($senactprog_active == '1')
  {
	$command = escapeshellcmd('/var/www/SenAct/senactprog.py');
	$output = shell_exec($command);
	echo $output;
  }

  if($senactsen_active == '1')
    shell_exec("/var/www/SenAct/startsen.sh");

//  header("Location: settings.html"); /* Redirect browser */
//  exit();
  return "<a href='senact.html'>Domov</a>   <a href='settings.html'>Spremeni naslednjega</a>";
}

function GetMyConnection()
{
    global $g_link;
    if( $g_link )
        return $g_link;
    $g_link = mysql_connect( 'localhost', 'boris', 'tejkica00') or die('Could not connect to server.' );
    mysql_select_db('senact', $g_link) or die('Could not select database.');
    return $g_link;
}

function CleanUpDB()
{
    global $g_link;
    if( $g_link != false )
        mysql_close($g_link);
    $g_link = false;
}
?>