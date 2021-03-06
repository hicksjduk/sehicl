<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
include 'db.php';
$dbname = getdbname($season);
$max_pos = isset($team) ? null : 50;
$sql = <<< END
with 
params as
(select :lsel as league_select, :tsel as team_select, :max as max_pos),
player_data as
(select id, name, team, substr(name, instr(name, ' ') + 1) ||
substr(name, 1, instr(name, ' ') -1) as sort_key 
from player),
innings_data as
(select b.player, b.out, b.runs, b.runs * 10 + (1 - b.out) as sort_key 
from batting b, player_data p, team t, league l, params parms
where b.player = p.id
and p.team = t.id
and t.league = l.id
and (parms.league_select is null or instr(l.name, parms.league_select) <> 0)
and (parms.team_select is null or parms.team_select = t.id)
),
batting_data as
(select p.name as player_name, t.id as team_id, t.name as team_name,
count(*) as inns, count(*) - sum(d.out) as not_out, sum(d.runs) as runs, 
max(d.sort_key) as best, 
round(cast(sum(d.runs) as real) / sum(d.out), 2)
 as average, sum(d.runs) as sort_key, p.sort_key as name_sort_key
from innings_data d, player_data p, team t
where d.player = p.id
and p.team = t.id
group by d.player),
sort_key as
(select sort_key from batting_data order by sort_key desc limit 1 offset (select min (p.max_pos, count(*)) - 1 from params p, batting_data d))
select player_name, team_id, team_name, inns, not_out, runs, 
(best/10) || case when (best % 10) then '*' else '' end as hs, average, d.sort_key from batting_data d, params parms, sort_key sk
where (parms.max_pos is null or d.sort_key >= sk.sort_key)
order by d.sort_key desc, name_sort_key asc
END;
$db = new SQLite3($dbname, SQLITE3_OPEN_READONLY);
try
{
$stmt = $db->prepare($sql);
$stmt->bindValue(':lsel', $league, $league == null ? SQLITE3_NULL : SQLITE3_TEXT);
$stmt->bindValue(':tsel', $team, $team == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$stmt->bindValue(':max', $max_pos, $max_pos == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$result = $stmt->execute();
?>
<table id="batav">
<thead>
<tr>
<th class="position number"></th>
<th class="name">Name</th>
<?php if (!isset($team)) { ?>
<th class="teamName name">Team</th>
<?php } ?>
<th class="innings number">Inns</th>
<th class="notout number">NO</th>
<th class="runs number">Runs</th>
<th class="highscore number">HS</th>
<th class="average number">Average</th>
</tr>
</thead>
<?php
$pos = 0;
while($row = $result->fetchArray(SQLITE3_ASSOC))
{
	$pos++;
?>
<tr>
<td class="position number"><?= $row['sort_key'] != $last_sort_key ? $pos : '' ?></td>
<td class="name"><?= $row['player_name'] ?></td>
<?php if (!isset($team)) { ?>
<td class="teamName name">
<a href="page.php?id=teamAverages&team=<?= $row['team_id'] ?>#Batting"><?= $row['team_name'] ?></a>
</td>
<?php } ?>
<td class="innings number"><?= $row['inns'] ?></td>
<td class="notout number"><?= $row['not_out'] ?></td>
<td class="runs number"><?= $row['runs'] ?></td>
<td class="highscore number"><?= $row['hs'] ?></td>
<td class="average number"><?= is_numeric($row['average']) ? sprintf('%1.2f', $row['average']) : '' ?></td>
</tr>
<?php
	$last_sort_key = $row['sort_key'];
}
?>
</table>
<?php
}
finally
{
	$db->close();
}
