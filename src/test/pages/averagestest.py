'''
Created on 20 Aug 2013

@author: hicksj
'''
import unittest
from pages.averages import BattingAverages, BowlingAverages, TeamAverages,\
    Averages, TeamAveragesIndex
from reports.averagesreport import BatsmanInReport, BowlerInReport, AveragesReport
from test.testbase import TestBase
import datetime


class Test(TestBase):

    def testGetTableRowForBattingTeamNotIncludedPositionNotIncludedHighScoreOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, True)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamNotIncludedPositionNotIncludedHighScoreNotOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamNotIncludedPositionNotIncludedHighScoreNotOutAverageDoesNotExist(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 4, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">4</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamNotIncludedPositionIncludedHighScoreOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, True)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamNotIncludedPositionIncludedHighScoreNotOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamNotIncludedPositionIncludedHighScoreNotOutAverageDoesNotExist(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 4, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="innings number">4</td>
            <td class="notout number">4</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionNotIncludedHighScoreOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, True)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionNotIncludedHighScoreNotOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionNotIncludedHighScoreNotOutAverageDoesNotExist(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 4, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">4</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionIncludedHighScoreOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, True)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionIncludedHighScoreNotOutAverageExists(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 1, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">1</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number">8.67</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBattingTeamIncludedPositionIncludedHighScoreNotOutAverageDoesNotExist(self):
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.runs, row.notout, row.innings = (26, 4, 4)
        row.highScore, row.highScoreOut = (12, False)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BattingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td>
            <td class="innings number">4</td>
            <td class="notout number">4</td>
            <td class="runs number">26</td>
            <td class="highscore number">12*</td>
            <td class="average number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 0)
        row.bestRuns, row.bestWickets = (2, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/2</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsMultipleOf6AverageExistsEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 1)
        row.bestRuns, row.bestWickets = (2, 1)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/2</td>
            <td class="averagePerWicket number">2.00</td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsNotMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (95, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">15.5</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">8.21</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionNotIncludedBallsNotMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (62, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = False
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">10.2</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">12.58</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 0)
        row.bestRuns, row.bestWickets = (2, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/2</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsMultipleOf6AverageExistsEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 1)
        row.bestRuns, row.bestWickets = (2, 1)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/2</td>
            <td class="averagePerWicket number">2.00</td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsNotMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (95, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">15.5</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">8.21</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamNotIncludedPositionIncludedBallsNotMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (62, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = True
        includeTeam = False
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            
            <td class="overs number">10.2</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">12.58</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 0)
        row.bestRuns, row.bestWickets = (2, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/2</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsMultipleOf6AverageExistsEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 1)
        row.bestRuns, row.bestWickets = (2, 1)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/2</td>
            <td class="averagePerWicket number">2.00</td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsNotMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (95, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">15.5</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">8.21</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionNotIncludedBallsNotMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (62, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = False
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">10.2</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">12.58</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 0)
        row.bestRuns, row.bestWickets = (2, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/2</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsMultipleOf6AverageExistsEconomyRateDoesNotExist(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (0, 2, 1)
        row.bestRuns, row.bestWickets = (2, 1)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">0</td>
            <td class="runs number">2</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/2</td>
            <td class="averagePerWicket number">2.00</td>
            <td class="averagePerOver number"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (54, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">9</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">14.44</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsNotMultipleOf6AverageDoesNotExistEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (95, 130, 0)
        row.bestRuns, row.bestWickets = (22, 0)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">15.5</td>
            <td class="runs number">130</td>
            <td class="wickets number">0</td>
            <td class="bestBowling number">0/22</td>
            <td class="averagePerWicket number"></td>
            <td class="averagePerOver number">8.21</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowForBowlingTeamIncludedPositionIncludedBallsNotMultipleOf6AverageExistsEconomyRateExists(self):
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.position = 4
        row.balls, row.runs, row.wickets = (62, 130, 7)
        row.bestRuns, row.bestWickets = (22, 3)
        row.maintainInvariants()
        includePosition = True
        includeTeam = True
        result = BowlingAverages("").getTableRow(row, includePosition, includeTeam)
        expectedResult = """
        <tr>
            <td class="position number">4</td>
            <td class="name">J Hicks</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td> 
            <td class="overs number">10.2</td>
            <td class="runs number">130</td>
            <td class="wickets number">7</td>
            <td class="bestBowling number">3/22</td>
            <td class="averagePerWicket number">18.57</td>
            <td class="averagePerOver number">12.58</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetTableRowsForBattingNoMaxRowsOneTeamOnly(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        maxRows = None
        result = BattingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player2</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player4</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player1</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">80</td>
            <td class="highscore number">15</td>
            <td class="average number">80.00</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="name">Player5</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player6</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number">6</td>
            <td class="name">Player3</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">40</td>
            <td class="highscore number">15</td>
            <td class="average number">40.00</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBattingNoMaxRowsMultipleTeams(self):
        report = AveragesReport()
        report.teamName = None
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        maxRows = None
        result = BattingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player2</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player4</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player1</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">80</td>
            <td class="highscore number">15</td>
            <td class="average number">80.00</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="name">Player5</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player6</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number">6</td>
            <td class="name">Player3</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">40</td>
            <td class="highscore number">15</td>
            <td class="average number">40.00</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBattingMaxRowsOneTeamOnly(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        maxRows = 4
        result = BattingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player2</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player4</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player1</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">80</td>
            <td class="highscore number">15</td>
            <td class="average number">80.00</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="name">Player5</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player6</td>
            
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBattingMaxRowsMultipleTeams(self):
        report = AveragesReport()
        report.teamName = None
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        maxRows = 4
        result = BattingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player2</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player4</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">100</td>
            <td class="highscore number">15</td>
            <td class="average number">100.00</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player1</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">80</td>
            <td class="highscore number">15</td>
            <td class="average number">80.00</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="name">Player5</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player6</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
            </td> 
            <td class="innings number">3</td>
            <td class="notout number">2</td>
            <td class="runs number">60</td>
            <td class="highscore number">15</td>
            <td class="average number">60.00</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBowlingNoMaxRowsOneTeamOnly(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        maxRows = None
        result = BowlingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player4</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">38.25</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="name">Player2</td>
            
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">3/9</td>
            <td class="averagePerWicket number">53.25</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player6</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player7</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">5</td>
            <td class="name">Player3</td>
            
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">2</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">106.50</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">6</td>
            <td class="name">Player1</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">153.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">7</td>
            <td class="name">Player5</td>
            
            <td class="overs number">9.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">153.00</td>
            <td class="averagePerOver number">16.11</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBowlingNoMaxRowsMultipleTeams(self):
        report = AveragesReport()
        report.teamName = None
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        maxRows = None
        result = BowlingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player4</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">38.25</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="name">Player2</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">3/9</td>
            <td class="averagePerWicket number">53.25</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player6</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player7</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">5</td>
            <td class="name">Player3</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">2</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">106.50</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">6</td>
            <td class="name">Player1</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">153.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">7</td>
            <td class="name">Player5</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">9.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">1</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">153.00</td>
            <td class="averagePerOver number">16.11</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBowlingMaxRowsOneTeamOnly(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        maxRows = 4
        result = BowlingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player4</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">38.25</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="name">Player2</td>
            
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">3/9</td>
            <td class="averagePerWicket number">53.25</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player6</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player7</td>
            
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetTableRowsForBowlingMaxRowsMultipleTeams(self):
        report = AveragesReport()
        report.teamName = None
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        maxRows = 5
        result = BowlingAverages("").getTableRows(report, maxRows)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="name">Player4</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">38.25</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="name">Player2</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">4</td>
            <td class="bestBowling number">3/9</td>
            <td class="averagePerWicket number">53.25</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="name">Player6</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="name">Player7</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">14.3</td>
            <td class="runs number">153</td>
            <td class="wickets number">3</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">51.00</td>
            <td class="averagePerOver number">10.55</td>
        </tr>
        <tr>
            <td class="position number">5</td>
            <td class="name">Player3</td>
            <td class="teamName name">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
            </td>
            <td class="overs number">16.4</td>
            <td class="runs number">213</td>
            <td class="wickets number">2</td>
            <td class="bestBowling number">1/26</td>
            <td class="averagePerWicket number">106.50</td>
            <td class="averagePerOver number">12.78</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportDataForBowling(self):
        report = AveragesReport()
        report.teamName = None
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        maxRows = 5
        result = BowlingAverages("").getReportData(report, maxRows)
        expectedResult = """
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <p class="noprint">Click on a team to see the bowling averages for that team.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">38.25</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">3/9</td>
                    <td class="averagePerWicket number">53.25</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player7</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">5</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">2</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">106.50</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportDataForBatting(self):
        report = AveragesReport()
        report.teamName = None
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        maxRows = None
        result = BattingAverages("").getReportData(report, maxRows)
        expectedResult = """
        <p>Players are ranked by runs scored.</p>
        <p class="noprint">Click on a team to see the batting averages for that team.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">80</td>
                    <td class="highscore number">15</td>
                    <td class="average number">80.00</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">40</td>
                    <td class="highscore number">15</td>
                    <td class="average number">40.00</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportDataForTeam(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.innings, row.notout, row.runs = (4, 2, 432)
        row.highScore, row.highScoreOut = (40, False)
        row.maintainInvariants()
        report.battingAverages = [row]
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.balls, row.runs, row.wickets = (127, 100, 8)
        row.bestRuns, row.bestWickets = 12, 3
        row.maintainInvariants()
        report.bowlingAverages = [row]
        result = TeamAverages("").getReportData(report)
        expectedResult = """
        <h2>
            <a id="Batting">Batting</a>
        </h2>
        <p>Players are ranked by runs scored.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                     
                    <td class="innings number">4</td>
                    <td class="notout number">2</td>
                    <td class="runs number">432</td>
                    <td class="highscore number">40*</td>
                    <td class="average number">216.00</td>
                </tr>
            </tbody>
        </table>
        <h2>
            <a id="Bowling">Bowling</a>
        </h2>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                    
                    <td class="overs number">21.1</td>
                    <td class="runs number">100</td>
                    <td class="wickets number">8</td>
                    <td class="bestBowling number">3/12</td>
                    <td class="averagePerWicket number">12.50</td>
                    <td class="averagePerOver number">4.72</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForBattingAllMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        report.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        result = BattingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Final averages.</p>
        <p>Players are ranked by runs scored.</p>
        <p class="noprint">Click on a team to see the batting averages for that team.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">80</td>
                    <td class="highscore number">15</td>
                    <td class="average number">80.00</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">40</td>
                    <td class="highscore number">15</td>
                    <td class="average number">40.00</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportBodyForBattingSomeMatchesPlayedNoneToCome(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 2)
        report.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        report.toCome = 0
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        result = BattingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Includes all games up to and including 2nd March 2013.</p>
        <p>Players are ranked by runs scored.</p>
        <p class="noprint">Click on a team to see the batting averages for that team.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">80</td>
                    <td class="highscore number">15</td>
                    <td class="average number">80.00</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">40</td>
                    <td class="highscore number">15</td>
                    <td class="average number">40.00</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportBodyForBattingSomeMatchesPlayedOneToCome(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 2)
        report.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        report.toCome = 1
        report.battingAverages = []
        row = BatsmanInReport("p1", "Player1", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 80)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p2", "Player2", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p3", "Player3", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 40)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p4", "Player4", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 100)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p5", "Player5", "t1", "OPCS")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        row = BatsmanInReport("p6", "Player6", "t2", "Moores")
        report.battingAverages.append(row)
        row.innings, row.notout, row.runs = (3, 2, 60)
        row.highScore, row.highScoreOut = ("15", True)
        row.maintainInvariants()
        result = BattingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 2nd March 2013 (1 result to come).</p>
        <p>Players are ranked by runs scored.</p>
        <p class="noprint">Click on a team to see the batting averages for that team.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">100</td>
                    <td class="highscore number">15</td>
                    <td class="average number">100.00</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">80</td>
                    <td class="highscore number">15</td>
                    <td class="average number">80.00</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Moores</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">60</td>
                    <td class="highscore number">15</td>
                    <td class="average number">60.00</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">OPCS</a>
                    </td> 
                    <td class="innings number">3</td>
                    <td class="notout number">2</td>
                    <td class="runs number">40</td>
                    <td class="highscore number">15</td>
                    <td class="average number">40.00</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportBodyForBattingNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = None
        report.battingAverages = []
        result = BattingAverages("").getReportBody(report)
        expectedResult = """
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetStatusMessageNoMatchesPlayed(self):
        report = AveragesReport()
        report.lastCompleteMatchDate = None
        result = Averages("").getStatusMessage(report)
        self.assertEquals("", result)

    def testGetStatusMessageAllMatchesPlayed(self):
        report = AveragesReport()
        report.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        report.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        result = Averages("").getStatusMessage(report)
        expectedResult = """
        <p class="statusMessage">Final averages.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedNoneToCome(self):
        report = AveragesReport()
        report.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        report.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        report.toCome = 0
        result = Averages("").getStatusMessage(report)
        expectedResult = """
        <p class="statusMessage">Includes all games up to and including 3rd March 2013.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedOneToCome(self):
        report = AveragesReport()
        report.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        report.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        report.toCome = 1
        result = Averages("").getStatusMessage(report)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 3rd March 2013 (1 result to come).</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedMoreThanOneToCome(self):
        report = AveragesReport()
        report.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        report.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        report.toCome = 2
        result = Averages("").getStatusMessage(report)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 3rd March 2013 (2 results to come).</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForBowlingAllMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 5)
        report.lastScheduledMatchDate = datetime.date(2013, 3, 5)
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        result = BowlingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Final averages.</p>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <p class="noprint">Click on a team to see the bowling averages for that team.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">38.25</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">3/9</td>
                    <td class="averagePerWicket number">53.25</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player7</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">5</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">2</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">106.50</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">7</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">9.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">16.11</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForBowlingSomeMatchesPlayedNoneToCome(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 5)
        report.lastScheduledMatchDate = datetime.date(2013, 4, 5)
        report.toCome = 0
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        result = BowlingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Includes all games up to and including 5th March 2013.</p>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <p class="noprint">Click on a team to see the bowling averages for that team.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">38.25</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">3/9</td>
                    <td class="averagePerWicket number">53.25</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player7</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">5</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">2</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">106.50</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">7</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">9.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">16.11</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForBowlingSomeMatchesPlayedOneToCome(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = datetime.date(2013, 3, 5)
        report.lastScheduledMatchDate = datetime.date(2013, 4, 5)
        report.toCome = 1
        report.bowlingAverages = []
        row = BowlerInReport("p1", "Player1", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p2", "Player2", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 4)
        row.bestWickets, row.bestRuns = (3, 9)
        row.maintainInvariants()
        row = BowlerInReport("p3", "Player3", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (100, 213, 2)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p4", "Player4", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 4)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p5", "Player5", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (57, 153, 1)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p6", "Player6", "t2", "Moores")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        row = BowlerInReport("p7", "Player7", "t1", "OPCS")
        report.bowlingAverages.append(row)
        row.balls, row.runs, row.wickets = (87, 153, 3)
        row.bestWickets, row.bestRuns = (1, 26)
        row.maintainInvariants()
        result = BowlingAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 5th March 2013 (1 result to come).</p>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <p class="noprint">Click on a team to see the bowling averages for that team.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    <th class="teamName name">Team</th>
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">Player4</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">38.25</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="name">Player2</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">4</td>
                    <td class="bestBowling number">3/9</td>
                    <td class="averagePerWicket number">53.25</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="name">Player6</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Moores</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="name">Player7</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">3</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">51.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">5</td>
                    <td class="name">Player3</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">16.4</td>
                    <td class="runs number">213</td>
                    <td class="wickets number">2</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">106.50</td>
                    <td class="averagePerOver number">12.78</td>
                </tr>
                <tr>
                    <td class="position number">6</td>
                    <td class="name">Player1</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">14.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">10.55</td>
                </tr>
                <tr>
                    <td class="position number">7</td>
                    <td class="name">Player5</td>
                    <td class="teamName name">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">OPCS</a>
                    </td>
                    <td class="overs number">9.3</td>
                    <td class="runs number">153</td>
                    <td class="wickets number">1</td>
                    <td class="bestBowling number">1/26</td>
                    <td class="averagePerWicket number">153.00</td>
                    <td class="averagePerOver number">16.11</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForBowlingNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.lastCompleteMatchDate = None
        report.bowlingAverages = []
        result = BowlingAverages("").getReportBody(report)
        expectedResult = """
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForTeamAllMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.lastCompleteMatchDate = datetime.date(2013, 4, 2)
        report.lastScheduledMatchDate = datetime.date(2013, 4, 2)
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.innings, row.notout, row.runs = (4, 2, 432)
        row.highScore, row.highScoreOut = (40, False)
        row.maintainInvariants()
        report.battingAverages = [row]
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.balls, row.runs, row.wickets = (127, 100, 8)
        row.bestRuns, row.bestWickets = 12, 3
        row.maintainInvariants()
        report.bowlingAverages = [row]
        result = TeamAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Final averages.</p>
        <h2>
            <a id="Batting">Batting</a>
        </h2>
        <p>Players are ranked by runs scored.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                     
                    <td class="innings number">4</td>
                    <td class="notout number">2</td>
                    <td class="runs number">432</td>
                    <td class="highscore number">40*</td>
                    <td class="average number">216.00</td>
                </tr>
            </tbody>
        </table>
        <h2>
            <a id="Bowling">Bowling</a>
        </h2>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                    
                    <td class="overs number">21.1</td>
                    <td class="runs number">100</td>
                    <td class="wickets number">8</td>
                    <td class="bestBowling number">3/12</td>
                    <td class="averagePerWicket number">12.50</td>
                    <td class="averagePerOver number">4.72</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForTeamSomeMatchesPlayedNoneToCome(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.lastCompleteMatchDate = datetime.date(2013, 4, 2)
        report.lastScheduledMatchDate = datetime.date(2013, 4, 3)
        report.toCome = 0
        row = BatsmanInReport("p1", "J Hicks", "t1", "OPCS")
        row.innings, row.notout, row.runs = (4, 2, 432)
        row.highScore, row.highScoreOut = (40, False)
        row.maintainInvariants()
        report.battingAverages = [row]
        row = BowlerInReport("p1", "J Hicks", "t1", "OPCS")
        row.balls, row.runs, row.wickets = (127, 100, 8)
        row.bestRuns, row.bestWickets = 12, 3
        row.maintainInvariants()
        report.bowlingAverages = [row]
        result = TeamAverages("").getReportBody(report)
        expectedResult = """
        <p class="statusMessage">Includes all games up to and including 2nd April 2013.</p>
        <h2>
            <a id="Batting">Batting</a>
        </h2>
        <p>Players are ranked by runs scored.</p>
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                     
                    <td class="innings number">4</td>
                    <td class="notout number">2</td>
                    <td class="runs number">432</td>
                    <td class="highscore number">40*</td>
                    <td class="average number">216.00</td>
                </tr>
            </tbody>
        </table>
        <h2>
            <a id="Bowling">Bowling</a>
        </h2>
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="name">J Hicks</td>
                    
                    <td class="overs number">21.1</td>
                    <td class="runs number">100</td>
                    <td class="wickets number">8</td>
                    <td class="bestBowling number">3/12</td>
                    <td class="averagePerWicket number">12.50</td>
                    <td class="averagePerOver number">4.72</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyForTeamNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = "OPCS"
        report.lastCompleteMatchDate = None
        report.battingAverages = []
        report.bowlingAverages = []
        result = TeamAverages("").getReportBody(report)
        expectedResult = """
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentForBattingNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.leagueName = "Senior"
        report.lastCompleteMatchDate = None
        report.battingAverages = []
        result = BattingAverages("").getReportContent(report)
        expectedResult = """
        <h1>Senior Batting</h1>
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentForBowlingNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = None
        report.leagueName = "Colts Under-13"
        report.lastCompleteMatchDate = None
        report.bowlingAverages = []
        result = BowlingAverages("").getReportContent(report)
        expectedResult = """
        <h1>Colts Under-13 Bowling</h1>
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentForTeamNoMatchesPlayed(self):
        report = AveragesReport()
        report.teamName = "Sarisbury Athletic"
        report.leagueName = "Colts Under-13"
        report.lastCompleteMatchDate = None
        report.battingAverages = []
        report.bowlingAverages = []
        result = TeamAverages("").getReportContent(report)
        expectedResult = """
        <h1>Sarisbury Athletic (Colts Under-13)</h1>
        <p>Averages will be available once the season has started.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetContentForBatting(self):
        page = BattingAverages("batting")
        page.allParams = {"xmlFile": "data/2012-13.xml"}
        result = page.getContent()
        self.assertNotEqual(None, result)
        
    def testGetContentForBowling(self):
        page = BowlingAverages("bowling")
        page.allParams = {"xmlFile": "data/2012-13.xml", "league": "ColtsUnder16"}
        result = page.getContent()
        self.assertNotEqual(None, result)
        
    def testGetContentForTeam(self):
        page = TeamAverages("team")
        page.allParams = {"xmlFile": "data/2012-13.xml", "team": "IBMSouthHants"}
        result = page.getContent()
        self.assertNotEqual(None, result)
        
    def testGetTeamCell(self):
        team = ("t1", "OPCS")
        result = TeamAveragesIndex("").getTeamCell(team)
        expectedResult = """
        <tr>
            <td class="teamName">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1">OPCS</a>
            </td>
            <td class="batLink">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">Batting</a>
            </td>
            <td class="bowlLink">
                <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">Bowling</a>
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetLeagueCell(self):
        report = {}
        league = ("l1", "League 1")
        teams = []
        report[league] = teams
        teams.append(("t1", "OPCS"))
        teams.append(("t2", "Moores"))
        teams.append(("t3", "Millcomms"))
        result = TeamAveragesIndex("").getLeagueCell(report, league)
        expectedResult = """
        <td>
            <h3 class="divheading">League 1</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3">Millcomms</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2">Moores</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1">OPCS</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRow(self):
        report = {}
        leagues = []
        league = ("l1", "League 1")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t1", "OPCS"))
        teams.append(("t2", "Moores"))
        teams.append(("t3", "Millcomms"))
        league = ("l2", "League 2")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t4", "Rotherham"))
        teams.append(("t5", "Arsenal"))
        teams.append(("t6", "Fulham"))
        result = TeamAveragesIndex("").getRow(report, leagues)
        expectedResult = """
        <tr>
        <td>
            <h3 class="divheading">League 1</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3">Millcomms</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t3#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2">Moores</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1">OPCS</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        <td>
            <h3 class="divheading">League 2</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5">Arsenal</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6">Fulham</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6#Bowling">Bowling</a>
                    </td>
                </tr>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4">Rotherham</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRows(self):
        report = {}
        leagues = []
        league = ("l1", "League 9")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t1", "OPCS"))
        league = ("l2", "League 2")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t2", "Moores"))
        league = ("l3", "League 14")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t4", "Rotherham"))
        league = ("l4", "League 17")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t5", "Arsenal"))
        league = ("l5", "League 6")
        leagues.append(league)
        teams = []
        report[league] = teams
        teams.append(("t6", "Fulham"))
        result = TeamAveragesIndex("").getRows(report)
        expectedResult = """
        <tr>
        <td>
            <h3 class="divheading">League 2</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2">Moores</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t2#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        <td>
            <h3 class="divheading">League 6</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6">Fulham</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t6#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        </tr>
        <tr>
        <td>
            <h3 class="divheading">League 9</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1">OPCS</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t1#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        <td>
            <h3 class="divheading">League 17</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5">Arsenal</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t5#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        </tr>
        <tr>
        <td>
            <h3 class="divheading">League 14</h3>
            <table>
                <tr>
                    <td class="teamName">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4">Rotherham</a>
                    </td>
                    <td class="batLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4#Batting">Batting</a>
                    </td>
                    <td class="bowlLink">
                        <a href="/cgi-bin/page.py?id=teamAverages&team=t4#Bowling">Bowling</a>
                    </td>
                </tr>
            </table>
        </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetTableRowForBattingNameNotIncluded']
    unittest.main()