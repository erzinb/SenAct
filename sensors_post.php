
<?php
$g_link = false;
$id = $_POST['id'];
$returnString = $id.", ";
$name = $_POST['name'];
$returnString = $returnString.$name.", ";
$type = $_POST['type'];
$returnString = $returnString.$type.", ";
$k = $_POST['k'];
$returnString = $returnString.$k.", ";
$n = $_POST['n'];
$returnString = $returnString.$n.", ";
//echo $returnString;
echo Update($id,$name,$type,$k,$n);

function GetId($id)
{
	$conn = GetMyConnection();
	if($conn)
	{
      $sql = "SELECT * FROM sensors where sensorId='$id'";
	    $retval = mysql_query( $sql, $conn );
	}
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['sensorId'];
}

function Update($id,$name,$type,$k,$n)
{
	$conn = GetMyConnection();
	if($conn)
	{
		$getid=GetId($id);
    		if(!$k) $k='null';
		if(!$n) $n='null';
		if($getid)
    {
//      echo "Update...";
			$sql = "UPDATE sensors SET name='$name',type='$type',k=$k,n=$n WHERE sensorId='$id'";
    }
		else
			$sql = "INSERT INTO sensors (sensorId,name,type,T,k,n,last_change) VALUES('$id','$name','$type',20,$k,$n,'2015-10-15 13:58:00'";
//    echo $sql;
		$retval = mysql_query( $sql, $conn );
//    echo "retval: ".$retval;
	}
	CleanUpDB();
  header("Location: sensors.html"); /* Redirect browser */
  exit();
//  return "<a href='senact.html'>Domov</a>   <a href='sensors.html'>Spremeni naslednjega</a>";
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