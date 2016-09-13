
<?php
$g_link = false;
$passwd1 = $_POST['passwd1'];
$passwd2 = $_POST['passwd2'];

if($passwd1 == $passwd2)
  echo InsertUser($_POST['uname'],$passwd1);
else
  echo "Gesli nista enaki! Poskusi znova...";

function InsertUser($user_id,$password)
{
	$conn = GetMyConnection();
  if($conn)
  {
    $hash = md5($password);
	  $sql = "INSERT INTO mysql_auth (username, passwd, groups) VALUES('" . $user_id . "','" . $hash . "','senact')";
	  $retval = mysql_query( $sql, $conn );
    CleanUpDB();
  }
	return "Uporabnik dodan...  <a href='senact.html'>Domov</a>";
}

function GetMyConnection()
{
    global $g_link;
    if( $g_link )
        return $g_link;
    $g_link = mysql_connect( 'localhost', 'root', 'tejkica00') or die('Could not connect to server.' );
    mysql_select_db('http_auth', $g_link) or die('Could not select database.');
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
