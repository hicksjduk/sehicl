<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
include 'db.php';
$dbname = getdbname($season);
$sql = <<< END
with
params as (select :tsel as team_select, 6 as max_wickets, :maxm as max_matches),

matches as
(select id, date, time, court, 
case when m.home = p.team_select then 'H' else 'A' end as home_away,
case when m.home = p.team_select then m.away else m.home end as opponents
from match m, params p where p.team_select in (m.home, m.away)),

selected_matches as
(select id from matches
order by date asc, time asc
limit (select ifnull(max_matches, 100) from params)),

batted_innings as
(select i.match, i.runs, i.wickets, i.order_no = 1 as first
from innings i, selected_matches m, params p
where i.match = m.id and i.batting = p.team_select),

bowled_innings as
(select i.match, i.runs, i.wickets
from innings i, selected_matches m, params p
where i.match = m.id and i.batting <> p.team_select),

played_matches as
(select i1.match, i1.runs as runs_scored, i1.wickets as wickets_lost,
i2.runs as runs_conceded, i2.wickets as wickets_taken, i1.first
from batted_innings i1, bowled_innings i2
where i1.match = i2.match),

awarded_matches as
(select a.* from awarded_match a, selected_matches m where a.match = m.id),

played_outcomes as
(select m.match,
case when m.runs_scored > m.runs_conceded then 'W'
when m.runs_scored < m.runs_conceded then 'L'
else 'T' end as outcome
from played_matches m
),

margins as
(select m.match, o.outcome,
case 
when not o.outcome in ('W', 'L') then null
when (o.outcome = 'W') = (m.first) then abs(m.runs_scored - m.runs_conceded)
when o.outcome = 'W' then p.max_wickets - m.wickets_lost
else p.max_wickets - m.wickets_taken
end as margin,
case
when not o.outcome in ('W', 'L') then null
when (o.outcome = 'W') = (m.first) then 'R'
else 'W'
end as margin_type
from played_matches m, played_outcomes o, params p where m.match = o.match
),

result_texts as
(select match,
case 
when outcome is null then null
when outcome = 'T' then 'Tied'
else
case when outcome = 'W' then 'Won' else 'Lost' end ||
' by ' || margin || 
case when margin_type = 'R' then ' run' else ' wicket' end || 
case when margin = 1 then '' else 's' end
end as result
from margins
union all
select
a.match,
case when a.winner = p.team_select then 'Won' else 'Lost' end ||
' by default (' ||
a.reason || ')' as result
from awarded_matches a, params p
)

select m.*, t.name as opp_name, t.league as league, result
from team t, matches m left outer join result_texts r on r.match = m.id 
where m.opponents = t.id
order by date asc, time asc
END;
$db = new SQLite3($dbname, SQLITE3_OPEN_READONLY);
try
{
$stmt = $db->prepare($sql);
$stmt->bindValue(':tsel', $team, $team == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$stmt->bindValue(':maxm', $maxmatches, $maxmatches == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$result = $stmt->execute();
?>
<table id="teamfix">
<thead>
<tr>
<th class="date">Date</th>
<th class="time">Time</th>
<th class="court">Court</th>
<th class="opponent">Opponent</th>
<th class="homeAway">H/A</th>
</tr>
</thead>
<?php
while($row = $result->fetchArray(SQLITE3_ASSOC))
{
$in_date = $row['date'] . ' ' . $row['time'];
$date = strtotime($in_date);	
?>
<tr>
<td class="date"><?= date('jS M y', $date) ?></td>
<td class="time"><?= date('g:i', $date) ?></td>
<td class="court"><?= $row['court'] ?></td>
<td class="opponent"><a href="page.php?id=teamFixtures&team=<?= $row['opponents'] ?>"><?= $row['opp_name'] ?></a></td>
<td class="homeAway"><?= $row['home_away'] ?></td>
<td class="result">
<a href="page.php?id=leagueResults&league=<?= $row['league'] ?>#<?= $row['id'] ?>">
<?= isset($row['result']) ? $row['result'] : ''?>
</a></td>
</tr>
<?php
}
?>
</table>

<?php
}
finally
{
	$db->close();
}
