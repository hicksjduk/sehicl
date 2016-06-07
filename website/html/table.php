<?php
$qstr = getenv ( 'QUERY_STRING' );
parse_str ( $qstr );
include 'db.php';
$dbname = getdbname($season);
$sql = <<< END
with 

params as (select :lsel as league_select, :maxm as max_matches),

selected_league as
(select l.* from league l, params p
where l.name like ('% ' || league_select) or l.name like ('%-' || league_select)),

selected_team as
(select t.* from team t, selected_league l where t.league = l.id),

selected_match as
(select m.* from match m, selected_league l where m.league = l.id order by m.date asc, m.time asc limit ifnull((select max_matches from params), 100)),

deduction_data as
(select d.team, d.points, d.reason || ' - ' || d.points || 
(case when d.points = 1 then ' point ' else ' points ' end) || 'deducted' as reason from deduction d, selected_team t where d.team = t.id),

innings_data as
(select i.* from innings i, selected_match m where i.match = m.id),

team_in_match_data as
(select i.match, i.batting as team, i.runs, ifnull(i.wickets, r.max_wickets) as wickets,
case when ifnull(i.wickets, r.max_wickets) = r.max_wickets then 
ifnull(m.over_limit, r.max_overs) * r.balls_per_over else i.balls end as rr_balls,
(select i2.runs from innings_data i2 where i2.match = i.match and i2.batting <> i.batting) as runs_against,
(select coalesce(i2.wickets, r.max_wickets) from innings_data i2 where i2.match = i.match and i2.batting <> i.batting) as wickets_taken,
i.order_no = 2 as batting_second
from innings_data i, selected_match m, rules r where i.match = m.id),

played_match_data as
(select match, team, runs, rr_balls, 
runs > runs_against as won,
runs = runs_against as tied,
runs < runs_against as lost,
min(r.max_batting_points, max(runs-r.batting_point_threshold, 0) / r.batting_point_increment + (batting_second * (runs > runs_against) * (r.max_wickets - wickets))) as batting_points,
wickets_taken as bowling_points
from team_in_match_data tim, rules r),

awarded as
(select m.id as match, m.home as team, m.home = a.winner as won from selected_match m, awarded_match a where a.match = m.id
union all
select m.id as match, m.away as team, m.away = a.winner as won from selected_match m, awarded_match a where a.match = m.id),

awarded_match_data as
(select a.match, a.team as team, 0 as runs, 0 as rr_balls, a.won, 0 as tied, 1-a.won as lost, a.won * r.awarded_batting_points as batting_points, a.won * r.awarded_bowling_points as bowling_points from awarded a, rules r),

match_data as
(select * from played_match_data union all select * from awarded_match_data),

unplayed_match_data as
(select m.home as team from match m, selected_league l
where m.league = l.id
and not exists(select md.match from match_data md where md.match = m.id)
union all
select m.away as team from match m, selected_league l
where m.league = l.id
and not exists(select md.match from match_data md where md.match = m.id)),

unplayed_match_counts as
(select team, count(*) as count from unplayed_match_data group by team),

table_data as
(select t.id as team, ifnull(sum(d.won), 0) as won, ifnull(sum(d.tied), 0) as tied, ifnull(sum(d.lost), 0) as lost, ifnull(sum(d.batting_points), 0) as batting_points, ifnull(sum(d.bowling_points), 0) as bowling_points,
ifnull(sum(d.runs), 0) as runs, sum(d.rr_balls) as rr_balls, 
(select sum(pd.points) from deduction_data pd where pd.team = t.id) as deductions,
(select group_concat(pd.reason, '//') from deduction_data pd where pd.team = t.id) as deduction_reasons
from selected_team t left outer join match_data d on t.id = d.team
group by t.id),

full_table as
(select d.team, t.name, d.won + d.tied + d.lost as played,
d.won, d.tied, d.lost, d.batting_points, d.bowling_points, 
d.runs, d.rr_balls,
1.0 * r.balls_per_over * d.runs / d.rr_balls as run_rate, d.deductions,
d.deduction_reasons,
d.won * r.win_points + d.tied * r.tie_points + d.batting_points + d.bowling_points - ifnull(d.deductions, 0) as points
from table_data d, selected_team t, rules r
where d.team = t.id and not t.excluded_from_tables),

min_max as
(select t.team, t.points +
ifnull(u.count, 0)
* (r.win_points + r.max_batting_points + r.max_wickets) as max_points,
t.points as min_points,
case when ifnull(u.count, 0) = 0 then t.run_rate else 99999 end as max_run_rate,
case when ifnull(u.count, 0) = 0 then t.run_rate else 1.0 * r.balls_per_over * t.runs / (t.rr_balls + u.count * r.max_overs * r.balls_per_over) end as min_run_rate
from full_table t, rules r
left outer join unplayed_match_counts u on u.team = t.team),

full_table_with_flags as
(select t.*,
(select count(*) from min_max mx 
where mx.team <> t.team 
and (mx.max_points > t.points 
or (mx.max_points = t.points and mx.max_run_rate >= mm.min_run_rate))) 
= 0 as champions,
(select count(*) from min_max mx 
where mx.team <> t.team 
and (mx.max_points > mm.min_points 
or (mx.max_points = mm.min_points and mx.max_run_rate >= mm.min_run_rate)))
< l.promoted as promoted,
(select count(*) from min_max mx 
where mx.team <> t.team 
and (mx.min_points < mm.max_points 
or (mx.min_points = mm.max_points and mx.min_run_rate <= mm.max_run_rate)))
< l.relegated as relegated
from full_table t, selected_league l, min_max mm where t.team = mm.team)

select * from full_table_with_flags
order by points desc, run_rate desc
END;
$db = new SQLite3($dbname, SQLITE3_OPEN_READONLY);
try
{
$stmt = $db->prepare($sql);
$stmt->bindValue(':lsel', $league, $league == null ? SQLITE3_NULL : SQLITE3_TEXT);
$stmt->bindValue(':maxm', $maxmatches, $maxmatches == null ? SQLITE3_NULL : SQLITE3_INTEGER);
$result = $stmt->execute();
?>
<table id="table">
<thead>
<tr>
<th class="position number"></th>
<th class="teamname"></th>
<th class="played number">P</th>
<th class="won number">W</th>
<th class="tied number">T</th>
<th class="lost number">L</th>
<th class="batpoints number">Bat</th>
<th class="bowlpoints number">Bowl</th>
<th class="runrate number">RR</th>
<th colspan="2">Ded</th>
<th class="points number">Pts</th>
</tr>
</thead>
<?php
$pos = 0;
$deduction_reasons = array();
while($row = $result->fetchArray(SQLITE3_ASSOC))
{
	$pos++;
	$sort_key = sprintf("%d:%2.15f", $row['points'], is_numeric($row['run_rate']) ? $row['run_rate'] : 0);
	$string = $row['deduction_reasons'];
	$dedkeys = '';
	if (isset ( $string )) 
	{
		$keys = array();
		$strings = explode ( '//', $string );
		foreach ( $strings as $str ) 
		{
			$index = $deduction_reasons [$str];
			if (! isset ( $index )) 
			{
				$index = count ( $deduction_reasons ) + 1;
				$deduction_reasons [$str] = count ( $deduction_reasons ) + 1;
			}
			$keys[] = $index;
		}
		$dedkeys = "(" . implode(',', $keys) . ")";
	}
	$flag_styles = array();
	if ($row['champions']) $flag_styles[] = "champions";
	if ($row['promoted']) $flag_styles[] = "promoted";
	if ($row['relegated']) $flag_styles[] = "relegated";
	$row_flags = implode(" ", $flag_styles);
?>
<tr>
<td class="position number"><?= $sort_key != $last_sort_key ? $pos : '' ?></td>
<td class="teamname <?= $row_flags ?>">
<a href="/page.php?id=teamFixtures&team=<?= $row['team'] ?>"><?= $row['name'] ?></a>
</td>
<td class="played number"><?= $row['played'] ?></td>
<td class="won number"><?= $row['won'] ?></td>
<td class="tied number"><?= $row['tied'] ?></td>
<td class="lost number"><?= $row['lost'] ?></td>
<td class="batpoints number"><?= $row['batting_points'] ?></td>
<td class="bowlpoints number"><?= $row['bowling_points'] ?></td>
<td class="runrate number"><?= is_numeric($row['run_rate']) ? sprintf('%1.2f', $row['run_rate']) : '' ?></td>
<td class="dedpoints number"><?= is_numeric($row['deductions']) ? $row['deductions'] : '' ?></td>
<td class="dedkeys"><?= $dedkeys ?></td>
<td class="points number"><?= $row['points'] ?></td>
</tr>
<?php
	$last_sort_key = $sort_key;
}
?>
</table>

<?php
}
finally
{
	$db->close();
}
if (count($deduction_reasons) > 0)
{
?>
<ul class="deductions">
<?php
foreach ($deduction_reasons as $string => $key)
{
?>
<li>
<span class="dedkeys"><?= "($key)" ?></span>
<?= $string ?>.
</li>
<?php
}
?>
</ul>
<?php
}
