<?php
function getdbname($season)
{
	$default = 16;
	if (!isset($season))
	{
		$season = $default;
	}
	$dbname = sprintf('../db/%d-%02d.db', $season + 1999, $season);
	return $dbname;
}

