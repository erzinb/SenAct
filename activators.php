<?php
// we'll generate XML output
header('Content-Type: text/xml');
// generate XML header
echo '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
// create the <response> element
// retrieve gpio, action and value
echo '<response>';
$id = $_GET['id'];

$g_link = false;

if($id == "all")
{
	echo GetAllActivators();
}
else if($id == "programs")
{
	echo GetPrograms();
}
else if($id == "settings")
{
	echo GetSettings();
}
else
{
	$action = $_GET['action'];
	$value = $_GET['value'];
	$block = $_GET['block'];
	$gpio = GetGpio($id);
	$type = GetActivatorType($id);
	    
	// setup the command
	$cmd = "gpio ";
	$cmd .= $action;
	$cmd .= " ";
	$cmd .= $gpio;
	$cmd .= " ";
	$cmd .= $value;
	$sqloutput = MySqlExec($action, $id, $value, $block, $type);
	echo "<pre>MySql response: ".$sqloutput."</pre>";
	if($sqloutput == "Updated Blocked")
	{
		shell_exec ( "/var/www/SenAct/block.sh " . $id . " " . $block . " > /dev/null 2>&1 &");
//		$output = shell_exec ( "/var/www/SenAct/block.sh " . $id . " 3.5");
//		echo "<pre>".$output."</pre>";
	}
	if($sqloutput != "Blocking")
	{
		if(($action == "write") && ($type == 1))
		{
			$toggle = GetToggleTime($id)/1000;
			shell_exec ( "/var/www/SenAct/toggle.sh " . $id . " " . $gpio . " " . $value . " " . $toggle . " > /dev/null 2>&1 &");
//			shell_exec ( "/var/www/SenAct/toggle.sh " . $id . " " . $gpio . " " . $value . " " . $toggle );
		}
		else
		{
			$output = shell_exec ( $cmd );
			echo "<pre>Command: " . $cmd . " executed. " . $output . "</pre>";
		}
	}
}
CleanUpDB();

// close the <response> element
echo '</response>';

function MySqlExec($action, $id, $value, $block, $type)
{
	$conn=GetMyConnection();

	if( $action == "write" )
	{
		if( !GetBlocking($id) )
		{
			$currentstate = GetState($id);
			if( $type == 1 )
			{
				$currentstate += 2;
			}
			else
				$currentstate = $value;
			$sql = "UPDATE activators SET state=$currentstate";
			$retval="Updated";
			if( $block )
			{
				if( $block > 0 )
				{
					$dtb = new Datetime();
					$dtb->add(new DateInterval("PT".$block."S"));
					$sql .= ", block_till='" . $dtb->format('Y-m-d H:i:s') . "', blocking=1";
					$retval .= " Blocked";
				}
			}

			$sql .= " WHERE id=$id";
			$retval1 = mysql_query( $sql, $conn );
			if(! $retval1 )
			{
				$retval = "Could not update data: " . $sql . mysql_error();
			}
		
			return $retval;
		}
		else
		{
			return "Blocking";
		}
	}
	else if($action=="read")
	{
		$sql = "SELECT state from activators where id=$id";
		$retval = mysql_query( $sql, $conn );
		$row = mysql_fetch_array($retval, MYSQL_ASSOC);
		return $row['state'];
	}
	return "Not supported";
}

function SetBlocking($id,$blocking)
{
	$conn = GetMyConnection();
	$sql = "UPDATE activators SET blocking=$blocking WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	return $retval;
}

function SetState($id,$state)
{
	$conn = GetMyConnection();
	$sql = "UPDATE activators SET state=$state WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	return $retval;
}

function GetBlocking($id)
{
	$conn = GetMyConnection();
	$sql = "SELECT blocking FROM activators WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['blocking'];
}

function GetActivatorType($id)
{
	$conn = GetMyConnection();
	$sql = "SELECT type FROM activators WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['type'];
}

function GetState($id)
{
	$conn = GetMyConnection();
	$sql = "SELECT state FROM activators WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['state'];
}

function GetToggleTime($id)
{
	$conn = GetMyConnection();
	$sql = "SELECT toggle_time_ms FROM activators WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['toggle_time_ms'];
}

function GetSettings()
{
	$conn = GetMyConnection();
	
	$sql = "SELECT * FROM senact_cntrl";
	$dbresult = mysql_query( $sql, $conn );
	$retval = "";
	
	if($dbresult )
	{
		$retval .= "<settings>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<setting>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</setting>";

		} // while

		$retval .= "</settings>";
	}

	return $retval;
}

function GetPrograms()
{
	$conn = GetMyConnection();
	
	$sql = "SELECT distinct a.id as id, b.name as Aktivator,case when a.sensorId = 'null' then null else c.name end as Senzor, case when a.TON = 'null' then null else a.TON end as TON, case when a.TOFF = 'null' then null else a.TOFF end as TOFF, a.start_time as Start,a.stop_time as Stop,a.month as Mesec,a.week as Teden,a.day as Dan,a.dayinweek as Dan_tedna FROM programs a, activators b, sensors c where a.activatorId=b.id and (a.sensorId = 'null' or a.sensorId=c.sensorId) order by b.name, c.name, a.start_time, a.stop_time, a.month, a.week, a.day, a.dayinweek";
	$dbresult = mysql_query( $sql, $conn );
	$retval = "";
	
	if($dbresult )
	{
		$retval .= "<programs>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<program>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</program>";

		} // while

		$retval .= "</programs>";
	}

	$sql = "SELECT id,name FROM activators";
	$dbresult = mysql_query( $sql, $conn );
		
	if($dbresult )
	{
		$retval .= "<activators>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<activator>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</activator>";

		} // while

		$retval .= "</activators>";
	}

	$sql = "SELECT sensorId as id,name FROM sensors";
	$dbresult = mysql_query( $sql, $conn );

	if($dbresult )
	{
		$retval .= "<sensors>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<sensor>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</sensor>";

		} // while

		$retval .= "</sensors>";
	}

	return $retval;
}

function GetAllActivators()
{
	$conn = GetMyConnection();
	
	$sql = "SELECT * FROM activators";
	$dbresult = mysql_query( $sql, $conn );
	$retval = "";
	
	if($dbresult )
	{
		$retval .= "<activators>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<activator>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</activator>";

		} // while

		$retval .= "</activators>";
	}
	
	$sql = "SELECT * FROM sensors";
	$dbresult = mysql_query( $sql, $conn );
		
	if($dbresult )
	{
		$retval .= "<sensors>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<sensor>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</sensor>";

		} // while

		$retval .= "</sensors>";
	}

	$sql = "select distinct a.name as ACTIVATOR, a.id as ID, a.state as STATE, case when c.sensorId = 'null' then null else b.name end as SENSOR, case when c.sensorId = 'null' then null else b.T end as T, case when c.TON = 'null' then null else c.TON end as TON, case when c.TOFF = 'null' then null else c.TOFF end as TOFF, c.start_time as START, c.stop_time as STOP, c.month as MESEC, c.week as TEDEN, c.day as DAN, c.dayinweek as DANTEDNA from programs c,activators a, sensors b where c.start_time<TIME(NOW()) and c.stop_time>=TIME(NOW()) and (c.month is null or c.month=MONTH(NOW())) and (c.week is null or c.week=WEEKOFYEAR(now())) and (c.day is null or c.day=day(now())) and (c.dayinweek is null or c.dayinweek=dayofweek(now())) and (c.activatorId=a.id) and (c.sensorId = 'null' or c.sensorId=b.sensorId) order by a.name, b.name, c.start_time, c.stop_time, c.month, c.week, c.day, c.dayinweek";
	$dbresult = mysql_query( $sql, $conn );
		
	if($dbresult )
	{
		$retval .= "<programs>";

		while($row = mysql_fetch_assoc($dbresult)) {
  
			$retval .= "<program>";

			// add a child node for each field
			foreach ($row as $fieldname => $fieldvalue) {
				$retval .= "<$fieldname>";
				$retval .= $fieldvalue;
				$retval .= "</$fieldname>";
			} // foreach

			$retval .= "</program>";

		} // while

		$retval .= "</programs>";
	}

	return $retval;
}

function GetGpio($id)
{
	$conn = GetMyConnection();
	$sql = "SELECT gpio FROM activators WHERE id=$id";
	$retval = mysql_query( $sql, $conn );
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['gpio'];
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