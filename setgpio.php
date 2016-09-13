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
$block = $_GET['block'];
// setup the command
$cmd = "gpio ";
$cmd .= $action;
$cmd .= " ";
$cmd .= $gpio;
$cmd .= " ";
$cmd .= $value;
$output = shell_exec ( $cmd );
echo "<pre>Command: ".$cmd." executed. ".$output."</pre>";
$sqloutput = mysqlexec($action, $gpio, $value, $block);
echo "<pre>MySql response: ".$sqloutput."</pre>";

// close the <response> element
echo '</response>';

function mysqlexec($action, $gpio, $value, $block)
{
	$dbhost = 'localhost';
	$dbuser = 'boris';
	$dbpass = 'tejkica00';
	$conn = mysql_connect($dbhost, $dbuser, $dbpass);
	if(! $conn )
	{
		return "Could not connect: " . mysql_error();
	}

	mysql_select_db('senact');

	if($action=="write")
	{
		if(!mysqlgetblocking($conn, $gpio))
		{
			$sql = "UPDATE activators SET state=$value";

			if($block)
			{
				if($block > 0)
				{
					$dtb = new Datetime();
					$dtb->add(new DateInterval("PT".$block."S"));
					$sql .= ", block_till='" . $dtb->format('Y-m-d H:i:s') . "', blocking=1";
					$blk = new Block();
					$blk->start();
				}
			}

			$sql .= " WHERE gpio=$gpio";
			$retval = mysql_query( $sql, $conn );
			if(! $retval )
			{
				$retval = "Could not update data: " . $sql . mysql_error();
				mysql_close($conn);
				return $retval;
			}
		

			mysql_close($conn);
			return "Updated";
		}
		else
		{
			mysql_close($conn);
			return "Blocking";
		}
	}
	else if($action=="read")
	{
		$sql = "SELECT state from activators where gpio=$gpio";
		$retval = mysql_query( $sql, $conn );
		mysql_close($conn);
		$row = mysql_fetch_array($retval, MYSQL_ASSOC);
		return $row['state'];
	}
	mysql_close($conn);
	return "Not supported";
}

function mysqlgetblocking($conn, $gpio)
{
	$sql = "SELECT blocking FROM activators WHERE gpio=$gpio";
	$retval = mysql_query( $sql, $conn );
	if(! $retval )
	{
		return false;
	}
	$row = mysql_fetch_array($retval, MYSQL_ASSOC);
	return $row['blocking'];
}

class Block extends Thread {
	public $seconds = 0;
//	public $conn = 0;
//	public $gpio = 0;
//	function __construct($c, $g, $s)
//	{
//		$conn = $c;
//		$gpio = $g;
//		$seconds = $s;
//	}
    public function run() {
        sleep($seconds);
//		$sql = "UPDATE activators SET blocking=0 where gpio=$gpio";
//		$retval = mysql_query( $sql, $conn );
    }
}
?>
