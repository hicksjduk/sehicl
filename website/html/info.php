<html>
<head>
<title>Hello World</title>
</head>
<body>
<?php
$filename = "../db/2015-16.db";
try {
$db = new SQLite3($filename, SQLITE3_OPEN_READONLY);
}
catch (Exception $e)
{
echo $e->getMessage(), " ", $e->getCode(), "\n";
}
$result = $db->query("select league.name, team.name from team, league where team.league = league.id order by league.name, team.name");
?>
<table>
<?php
while ($row = $result->fetchArray()) {
$index = 0;
?>
<tr><td><?= $row[$index++] ?></td><td><?= $row[$index++] ?></td></tr>
<?php
}
?>
</table>
</p>
<?php phpinfo(); ?>
</body>
</html>
