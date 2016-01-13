<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
include 'db.php';
$dbname = getdbname($season);
$sql = <<< END
with params as (select :lsel as league_select, :maxp as max_played),

selected_leagues as
(select l.* from league l, params p 
where p.league_select is null
or l.name like '% ' || p.league_select
or l.name like '%-' || p.league_select
),

selected_matches as
(select m.id, m.league, m.home, m.away, m.date, m.time, m.court, l.name as league_name, t1.name as home_name, t2.name as away_name from match m, selected_leagues l, team t1, team t2
where m.league = l.id
and m.home = t1.id
and m.away = t2.id
),

logically_unplayed_matches as
(select id from selected_matches
order by date asc, time asc
limit 1000 offset (select ifnull(max_played, 1000) from params)
),

actually_unplayed_matches as
(select id from selected_matches
where id not in (select distinct match from innings union all select match from awarded_match)
),

unplayed_matches as (select * from logically_unplayed_matches union all 
select * from actually_unplayed_matches)

select m.* from selected_matches m, unplayed_matches um where m.id = um.id
order by date, time, court, home_name
END;
$db = new SQLite3($dbname, SQLITE3_OPEN_READONLY);
try
{
$stmt = $db->prepare($sql);
$stmt->bindValue(':lsel', $league, $league == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$stmt->bindValue(':maxp', $maxplayed, $maxplayed == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$result = $stmt->execute();
if (!$result->fetchArray(SQLITE3_ASSOC))
{
?>
<p>There are no outstanding fixtures at present.</p>
<?php
}
else
{
	$result->reset();
?>
<p class="noprint">Click on a team to see all matches for that team, or on a division to see all matches for that division.</p>
<table id="fixlist">
<?php
while($row = $result->fetchArray(SQLITE3_ASSOC))
{
$in_date = $row['date'] . ' ' . $row['time'];
$date = strtotime($in_date);
$datestr = date('jS F Y', $date);	
if ($datestr != $last_date)
{
    $last_date = $datestr;
    $last_time = null;
?>
<tr>
<td class="date" colspan="3"><?= $datestr ?></td>
</tr>
<?php
} 
?>
<tr>
<?php
$thetime = "&nbsp;";
$timestr = date('g:i', $date); 
if ($timestr != $last_time)
{
	$last_time = $timestr;
	$thetime = $timestr;
}
?>
<td class="time"><?= $thetime ?></td>
<td class="court"><?= $row['court'] ?></td>
<td class="teams">
<a href="page.php?id=teamFixtures&team=<?= $row['home'] ?>"><?= $row['home_name'] ?></a>
v
<a href="page.php?id=teamFixtures&team=<?= $row['away'] ?>"><?= $row['away_name'] ?></a>
</td>
<?php
if (league != null)
{
?>
<td class="division">
<a href="page.php?id=leagueFixtures&league=<?= $row['league'] ?>"><?= $row['league_name'] ?></a>
</td>
<?php
}
?>
</tr>
<?php
}
?>
</table>

<?php
}
}
finally
{
	$db->close();
}
