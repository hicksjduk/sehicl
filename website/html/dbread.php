<html>
<head>
<title>Hello World</title>
</head>
<body>
<?= getcwd() ?>
<?php
$db = new SQLite3("../db/2015-16.db");
$result = $db->query("select name from team");
var_dump($result->fetchArray());
?>
<p>
<?php
$result = $db->query("with version as (select sqlite_version()) select * from version");
var_dump($result->fetchArray());
?>
<p>
<?php phpinfo(); ?>
</body>
</html>
