
<?php
$g_link = false;
$id = $_POST['id'];
$returnString = $id.", ";
$gpio = $_POST['gpio'];
$returnString = $returnString.$gpio.", ";
$name = $_POST['name'];
$returnString = $returnString.$name.", ";
$type = $_POST['type'];
$returnString = $returnString.$type.", ";
$toggle_time = $_POST['toggle_time_ms'];
$returnString = $returnString.$toggle_time;
//echo $returnString;
echo Update($id,$name,$gpio,$type,$toggle_time);

function GetId($id)
{
	$conn = GetMyConnection();
	if($conn)
	{
      $sql = "SELECT * FROM activators where id=$id";
	    $retval = mysql_query( $sql, $conn );
	}
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['id'];
}

function Update($id,$name,$gpio,$type,$toggle_time)
{
	$conn = GetMyConnection();
	if($conn)
	{
		$getid=GetId($id);
    
		if($getid)
    {
//      echo "Update...";
			$sql = "UPDATE activators SET name='$name',gpio=$gpio,type=$type,toggle_time_ms=$toggle_time WHERE id='$id'";
    }
		else
			$sql = "INSERT INTO activators (id,name,gpio,type,toggle_time_ms,state,blocking) VALUES($id,$name,$gpio,$type,$toggle_time,0,0";
		$retval = mysql_query( $sql, $conn );
//    echo "retval: ".$retval;
	}
	CleanUpDB();
  header("Location: activators.html"); /* Redirect browser */
  exit();
//  return "<a href='senact.html'>Domov</a>   <a href='activators.html'>Spremeni naslednjega</a>";
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