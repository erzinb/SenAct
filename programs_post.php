
<?php
$g_link = false;
$id = $_POST['id'];
$activatorId = $_POST['activator'];
if(empty($activatorId))
	$activatorId='null';
$sensorId = $_POST['sensor'];
if (empty($sensorId))
	$sensorId='null';
$ton = $_POST['ton'];
if (empty($ton))
	$ton='null';
$toff = $_POST['toff'];
if (empty($toff))
	$toff='null';
$start = $_POST['start'];
if (empty($start))
	$start='null';
$stop = $_POST['stop'];
if (empty($stop))
	$stop='null';
$mesec = $_POST['mesec'];
if (empty($mesec))
	$mesec='null';
$teden = $_POST['teden'];
if (empty($teden))
	$teden='null';
$dan = $_POST['dan'];
if (empty($dan))
	$dan='null';
$dantedna = $_POST['dantedna'];
if (empty($dantedna))
	$dantedna='null';

/*$returnString = $id.", ";
$returnString = $returnString.$activatorId.", ";
$returnString = $returnString.$sensorId.", ";
$returnString = $returnString.$ton.", ";
$returnString = $returnString.$toff.", ";
$returnString = $returnString.$start.", ";
$returnString = $returnString.$stop.", ";
$returnString = $returnString.$mesec.", ";
$returnString = $returnString.$teden.", ";
$returnString = $returnString.$dan.", ";
$returnString = $returnString.$dantedna.", ";
echo $returnString;
*/

if ($_POST['action'] == 'Spremeni') {
	echo Update($id,$activatorId,$sensorId,$ton,$toff,$start,$stop,$mesec,$teden,$dan,$dantedna);
} else if ($_POST['action'] == 'Dodaj') {
	echo Insert($activatorId,$sensorId,$ton,$toff,$start,$stop,$mesec,$teden,$dan,$dantedna);
} else {
	echo Delete($id);
}

function Update($id,$activatorId,$sensorId,$ton,$toff,$start,$stop,$mesec,$teden,$dan,$dantedna)
	{
	$conn = GetMyConnection();
	if($conn)
	{
		if($id)
		{
	//		echo "Update...";
			$sql = "UPDATE programs SET activatorId=$activatorId,sensorId='$sensorId',TON=$ton,TOFF=$toff,start_time='$start',stop_time='$stop',month=$mesec,week=$teden,day=$dan,dayinweek=$dantedna WHERE id=$id";
		//	echo $sql;
		}
		$retval = mysql_query( $sql, $conn );
//		echo "retval: ".$retval;
	}
	CleanUpDB();
	header("Location: programs.html"); /* Redirect browser to programs.html*/
	exit();
	//  return "<a href='senact.html'>Domov</a>   <a href='programs.html'>Spremeni naslednjega</a>";
	}

function Insert($activatorId,$sensorId,$ton,$toff,$start,$stop,$mesec,$teden,$dan,$dantedna)
	{
	$conn = GetMyConnection();
	if($conn)
	{
		$sql = "INSERT INTO programs (activatorId,sensorId,TON,TOFF,start_time,stop_time,month,week,day,dayinweek) VALUES($activatorId,'$sensorId',$ton,$toff,'$start','$stop',$mesec,$teden,$dan,$dantedna)";
		//    echo $sql;
		$retval = mysql_query( $sql, $conn );
		//    echo "retval: ".$retval;
	}
	CleanUpDB();
	header("Location: programs.html"); /* Redirect browser */
	exit();
	//  return "<a href='senact.html'>Domov</a>   <a href='sensors.html'>Spremeni naslednjega</a>";
	}

function Delete($id)
	{
	$conn = GetMyConnection();
	if($conn)
	{
		if($id)
		{
			$sql = "DELETE from programs WHERE id=$id";
			//    echo $sql;
			$retval = mysql_query( $sql, $conn );
			//    echo "retval: ".$retval;
		}
	}
	CleanUpDB();
	header("Location: programs.html"); /* Redirect browser */
	exit();
	//  return "<a href='senact.html'>Domov</a>   <a href='programs.html'>Spremeni naslednjega</a>";
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