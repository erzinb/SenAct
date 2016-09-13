
<?php
$g_link = false;
$data = $_POST['data'];
$returnString = $data;
//echo $returnString;
echo GetValidDate($data);
CleanUpDB();

function GetValidDate($data)
{
	$conn = GetMyConnection();
	if($conn)
	{
      $sql = "SELECT NOW()<valid_till as valid FROM licence where data='$data'";
	    $retval = mysql_query( $sql, $conn );
	}
  if( mysql_num_rows($retval) > 0 )
  {
	  $row = mysql_fetch_array($retval, MYSQL_ASSOC);
	  return $row['valid'];
  }
  else
    return '0';
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