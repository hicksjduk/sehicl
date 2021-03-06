<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
include 'db.php';
$dbname = getdbname($season);
$max_pos = isset ( $team ) ? null : 50;
$sql = <<< END
with
params as (select :lsel as league_select, :tsel as team_select, :max as max_pos),
innings_data as
(select b.player, b.balls, b.runs, b.wickets, 
printf('%d%.15f%d/%d', b.wickets, 10 - (cast(b.runs as real) / b.balls), 999 - b.runs, b.runs) as sort_key
from bowling b, player p, team t, league l, params parms
where b.player = p.id
and p.team = t.id
and t.league = l.id
and (parms.league_select is null or instr(l.name, parms.league_select) <> 0)
and (parms.team_select is null or parms.team_select = t.id)
),
bowling_data as
(
select p.name as player_name, t.id as team_id, t.name as team_name,
sum(b.balls) as balls, sum(b.runs) as runs, sum(b.wickets) as wickets,
round(cast(sum(b.runs) as real) / sum(b.wickets), 2) as average, round(cast(sum(b.runs) * 6 as real) / sum(b.balls), 2) as economy, max(b.sort_key) as best,
printf('%d%.15f', sum(b.wickets) + 10, 10 - (cast(sum(b.runs) as real) / sum(b.balls))) as sort_key
from innings_data b, player p, team t
where b.player = p.id
and p.team = t.id
group by player)
select player_name, team_id, team_name, balls / 6 + 0.1 * (balls % 6) as overs,
runs, wickets, average, economy,
substr(best,1,1) || substr(best,instr(best,'/')) as best_bowling, sort_key
from bowling_data d, params parms
where (parms.max_pos is null or d.sort_key >= 
(select sort_key from bowling_data order by sort_key desc limit 1 offset
(select min(p.max_pos, count(*)) from params p, bowling_data d)))
order by sort_key desc
END;
$db = new SQLite3 ( $dbname, SQLITE3_OPEN_READONLY );
try {
	$stmt = $db->prepare ( $sql );
	$stmt->bindValue ( ':lsel', $league, $league == null ? SQLITE3_NULL : SQLITE3_TEXT );
	$stmt->bindValue ( ':tsel', $team, $team == null ? SQLITE3_NULL : SQLITE3_INTEGER );
	$stmt->bindValue ( ':max', $max_pos, $max_pos == null ? SQLITE3_NULL : SQLITE3_INTEGER );
	$result = $stmt->execute ();
	?>
<table id="bowlav">
	<thead>
		<tr>
			<th class="position number"></th>
			<th class="name">Name</th>
<?php if (!isset($team)) { ?>
						<th class="teamName name">Team</th>
<?php } ?>
						<th class="overs number">Overs</th>
			<th class="runs number">Runs</th>
			<th class="runs number">Wickets</th>
			<th class="bestBowling number">Best</th>
			<th class="averagePerWicket number">Runs/wkt</th>
			<th class="averagePerOver number">Runs/over</th>
		</tr>
	</thead>
<?php
	$pos = 0;
	while ( $row = $result->fetchArray ( SQLITE3_ASSOC ) ) {
		$pos ++;
		?>
<tr>
		<td class="position number"><?= $row['sort_key'] != $last_sort_key ? $pos : '' ?></td>
		<td class="name"><?= $row['player_name'] ?></td>
<?php if (!isset($team)) { ?>
<td class="teamName name"><a
			href="page.php?id=teamAverages&team=<?= $row['team_id'] ?>#Batting"><?= $row['team_name'] ?></a>
		</td>
<?php } ?>
<td class="overs number"><?= $row['overs'] ?></td>
		<td class="runs number"><?= $row['runs'] ?></td>
		<td class="wickets number"><?= $row['wickets'] ?></td>
		<td class="bestBowling number"><?= $row['best_bowling'] ?></td>
		<td class="averagePerWicket number"><?= is_numeric($row['average']) ? sprintf('%1.2f', $row['average']) : '' ?></td>
		<td class="averagePerOver number"><?= is_numeric($row['economy']) ? sprintf('%1.2f', $row['economy']) : '' ?></td>
	</tr>
<?php
		$last_sort_key = $row ['sort_key'];
}
?>
</table>
<?php
}
finally
{
	$db->close();
}
