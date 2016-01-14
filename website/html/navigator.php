<?php 
include 'navigatorItem.php';
$items = 
[
	new NavigatorItem("home"),
	new NavigatorItem("contacts"),
	new NavigatorItem("fixtures"),
	new NavigatorItem("results"),
	new NavigatorItem("tables"),
	new NavigatorItem("averages"),
	new NavigatorItem("resources"),
	new NavigatorItem("rules"),
	new NavigatorItem("records"),
	new NavigatorItem("archive"),
]
?>
<ul class="navigator">
	<?php foreach ($items as $item) {?>
	<li><?= $item->getHtml($id); ?></li>
	<?php }?>
</ul>

