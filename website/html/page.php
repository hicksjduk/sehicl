<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
if ($id == "")
	$id = "home";
include 'mailto.php';
?>

<html>
<head>

<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link href="/sehicl2.css" rel="stylesheet" type="text/css">
<script language="javascript" src="/sehicl2.js" type="text/javascript"></script>
<title>South East Hampshire (Fareham) Indoor Cricket League</title>

</head>
<body id="home">

<div id="page">
<div id="leftNavigator">
<?php
include 'navigator.php';
?>
</div>

<div id="main">
<div id="header">

<p id="LeagueInfo">
<img src="/graphics/leaguelogo_red.gif" align="left" hspace="20" alt="South-East Hampshire (Fareham) Indoor Cricket League">
<span class="nolinewrap">South-East Hampshire (Fareham)</span> <span class="nolinewrap">Indoor Cricket League</span>
</p>
<p id="SponsorInfo">Sponsored by Game Set and Match
<a href="http://www.gsam.co.uk" target="_blank">
<img src="/graphics/smallgsamlogo.gif" align="middle" hspace="15" border="0" alt="Sponsored by Game Set and Match">
</a>
</p>

</div>
<div id="content">

Page content

</div>
<div id="footer">

<p>
<hr>
</p>
<p style="font-size: smaller">
<span style="font-weight: bold">
&copy; South-East Hampshire (Fareham) Indoor Cricket League
</span>
<br>
All rights reserved.
</p>
<p>
<a href="http://www.hants.gov.uk" target="_blank">
<img src="/images/credit/hosted-white.gif" align="middle" width="154" height="70" border="0" alt="Web Space provided by Hampshire County Council">
</a>
</p>

</div>
</div>
</div>

</body>
</html>
