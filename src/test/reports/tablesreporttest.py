'''
Created on 8 Aug 2013

@author: hicksj
'''
import unittest
from reports.tablesreport import LeagueTableReportGenerator, TableRow,\
    PointsDeduction
from xml.etree import ElementTree
import datetime


class Test(unittest.TestCase):

    def testCalculateBattingPointsScoreLessThan60NoWicketsPoints(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(59, None)
        self.assertEqual(0, result)

    def testCalculateBattingPointsScoreMoreThan60NoWicketsPoints(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(79, None)
        self.assertEqual(1, result)

    def testCalculateBattingPointsScoreLessThan60WicketsPoints(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(49, 5)
        self.assertEqual(1, result)

    def testCalculateBattingPointsScoreMoreThan60WicketsPoints(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(103, 4)
        self.assertEqual(6, result)

    def testCalculateBattingPointsScoreMoreThan129NoWicketsPoints(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(130, None)
        self.assertEqual(6, result)

    def testCalculateBattingPointsScoreTotalOfRunsAndWicketsPointsMoreThan6(self):
        result = LeagueTableReportGenerator().calculateBattingPoints(150, 1)
        self.assertEqual(6, result)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsForAbsentWicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsFor6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsForLessThan6WicketsAgainstAbsent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(6, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsForAbsentWicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsFor6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>6</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(6, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsAbsentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsAbsentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(72, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsAbsentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsAbsentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(66, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitAbsentBallsPresentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitAbsentBallsPresentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingFirstOverLimitPresentBallsPresentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(True, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)

    def testGetScoreDataBattingSecondOverLimitPresentBallsPresentWicketsForLessThan6WicketsAgainstPresent(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <runsScored>124</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = LeagueTableReportGenerator().getScoreData(playedMatchElement, "t1")
        self.assertEquals(False, batFirst)
        self.assertEquals(123, scoreFor)
        self.assertEquals(44, ballsFaced)
        self.assertEquals(5, wicketsLost)
        self.assertEquals(124, scoreAgainst)
        self.assertEquals(4, wicketsTaken)
        
    def testUpdateTableRowFromMatchDataWonBattingFirst(self):
        tableRow = TableRow(None, "Hello")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 60)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromMatchData(tableRow, True, 70, 62, None, 69, 4)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(2, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(3, tableRow.lost)
        self.assertEquals(170, tableRow.runs)
        self.assertEquals(122, tableRow.balls)
        self.assertAlmostEquals(8.361, tableRow.runrate, 3)
        self.assertEquals(11, tableRow.batpoints)
        self.assertEquals(24, tableRow.bowlpoints)
        self.assertEquals(65, tableRow.points)
        self.assertEquals("93489.639344262295083Hello", tableRow.sortKey)

    def testUpdateTableRowFromMatchDataWonBattingSecond(self):
        tableRow = TableRow(None, "Hello")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 60)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromMatchData(tableRow, False, 70, 62, 4, 69, 4)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(2, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(3, tableRow.lost)
        self.assertEquals(170, tableRow.runs)
        self.assertEquals(122, tableRow.balls)
        self.assertAlmostEquals(8.361, tableRow.runrate, 3)
        self.assertEquals(13, tableRow.batpoints)
        self.assertEquals(24, tableRow.bowlpoints)
        self.assertEquals(67, tableRow.points)
        self.assertEquals("93289.639344262295083Hello", tableRow.sortKey)

    def testUpdateTableRowFromMatchDataTied(self):
        tableRow = TableRow(None, "Hello")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 60)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromMatchData(tableRow, True, 70, 62, None, 70, 4)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(1, tableRow.won)
        self.assertEquals(3, tableRow.tied)
        self.assertEquals(3, tableRow.lost)
        self.assertEquals(170, tableRow.runs)
        self.assertEquals(122, tableRow.balls)
        self.assertAlmostEquals(8.361, tableRow.runrate, 3)
        self.assertEquals(11, tableRow.batpoints)
        self.assertEquals(24, tableRow.bowlpoints)
        self.assertEquals(59, tableRow.points)
        self.assertEquals("94089.639344262295083Hello", tableRow.sortKey)

    def testUpdateTableRowFromMatchDataLost(self):
        tableRow = TableRow(None, "Hello")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 60)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromMatchData(tableRow, True, 70, 62, None, 71, 4)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(1, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(4, tableRow.lost)
        self.assertEquals(170, tableRow.runs)
        self.assertEquals(122, tableRow.balls)
        self.assertAlmostEquals(8.361, tableRow.runrate, 3)
        self.assertEquals(11, tableRow.batpoints)
        self.assertEquals(24, tableRow.bowlpoints)
        self.assertEquals(53, tableRow.points)
        self.assertEquals("94689.639344262295083Hello", tableRow.sortKey)

    def testUpdateTableRowFromMatchDataBallsIsStillZero(self):
        tableRow = TableRow(None, "Hello")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 0)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromMatchData(tableRow, False, 3, 0, 0, 2, 6)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(2, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(3, tableRow.lost)
        self.assertEquals(103, tableRow.runs)
        self.assertEquals(0, tableRow.balls)
        self.assertEquals(-1, tableRow.runrate)
        self.assertEquals(16, tableRow.batpoints)
        self.assertEquals(26, tableRow.bowlpoints)
        self.assertEquals(72, tableRow.points)
        self.assertEquals("92799.000000000000000Hello", tableRow.sortKey)
        
    def testUpdateTableRowFromPlayedMatchTeamIsBattingFirst(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>110</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        tableRow = TableRow("t1", None)
        LeagueTableReportGenerator().updateTableRowFromPlayedMatch(tableRow, playedMatchElement)
        self.assertEquals(1, tableRow.played)
        self.assertEquals(1, tableRow.won)
        self.assertEquals(0, tableRow.tied)
        self.assertEquals(0, tableRow.lost)
        self.assertEquals(123, tableRow.runs)
        self.assertEquals(44, tableRow.balls)
        self.assertAlmostEquals(16.773, tableRow.runrate, 3)
        self.assertEquals(6, tableRow.batpoints)
        self.assertEquals(4, tableRow.bowlpoints)
        self.assertEquals(22, tableRow.points)
        
    def testUpdateTableRowFromPlayedMatchTeamIsBattingSecond(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>123</runsScored>
                    <wicketsLost>5</wicketsLost>
                    <ballsBowled>44</ballsBowled>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>110</runsScored>
                    <wicketsLost>4</wicketsLost>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        tableRow = TableRow("t2", None)
        LeagueTableReportGenerator().updateTableRowFromPlayedMatch(tableRow, playedMatchElement)
        self.assertEquals(1, tableRow.played)
        self.assertEquals(0, tableRow.won)
        self.assertEquals(0, tableRow.tied)
        self.assertEquals(1, tableRow.lost)
        self.assertEquals(110, tableRow.runs)
        self.assertEquals(72, tableRow.balls)
        self.assertAlmostEquals(9.167, tableRow.runrate, 3)
        self.assertEquals(5, tableRow.batpoints)
        self.assertEquals(5, tableRow.bowlpoints)
        self.assertEquals(10, tableRow.points)
        
    def testUpdateTableRowFromAwardedMatchTeamIsWinner(self):
        xml = """
        <awardedMatch>
            <winner id="t1"/>
        </awardedMatch>
        """
        awardedMatchElement = ElementTree.fromstring(xml)
        tableRow = TableRow("t1", "")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 0)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromAwardedMatch(tableRow, awardedMatchElement)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(2, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(3, tableRow.lost)
        self.assertEquals(100, tableRow.runs)
        self.assertEquals(0, tableRow.balls)
        self.assertEquals(-1, tableRow.runrate)
        self.assertEquals(13, tableRow.batpoints)
        self.assertEquals(26, tableRow.bowlpoints)
        self.assertEquals(69, tableRow.points)
        
    def testUpdateTableRowFromAwardedMatchTeamIsLoser(self):
        xml = """
        <awardedMatch>
            <winner id="t1"/>
        </awardedMatch>
        """
        awardedMatchElement = ElementTree.fromstring(xml)
        tableRow = TableRow("t2", "")
        tableRow.won, tableRow.tied, tableRow.lost = (1, 2, 3)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.runs, tableRow.balls = (100, 0)
        tableRow.deductions = [PointsDeduction(6, "")]
        LeagueTableReportGenerator().updateTableRowFromAwardedMatch(tableRow, awardedMatchElement)
        self.assertEquals(7, tableRow.played)
        self.assertEquals(1, tableRow.won)
        self.assertEquals(2, tableRow.tied)
        self.assertEquals(4, tableRow.lost)
        self.assertEquals(100, tableRow.runs)
        self.assertEquals(0, tableRow.balls)
        self.assertEquals(-1, tableRow.runrate)
        self.assertEquals(10, tableRow.batpoints)
        self.assertEquals(20, tableRow.bowlpoints)
        self.assertEquals(48, tableRow.points)
        
    def testGetTableRowsForMatchNeitherTeamFound(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        tableRows = {}
        for tid in ["t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getTableRowsForMatch(matchElement, tableRows)
        self.assertEquals([], result)
        
    def testGetTableRowsForMatchFirstTeamFound(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        tableRows = {}
        for tid in ["t1", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getTableRowsForMatch(matchElement, tableRows)
        self.assertEquals([tableRows["t1"]], result)
        
    def testGetTableRowsForMatchSecondTeamFound(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        tableRows = {}
        for tid in ["t2", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getTableRowsForMatch(matchElement, tableRows)
        self.assertEquals([tableRows["t2"]], result)
        
    def testGetTableRowsForMatchBothTeamsFound(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        tableRows = {}
        for tid in ["t1", "t2", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getTableRowsForMatch(matchElement, tableRows)
        self.assertEquals([tableRows["t1"], tableRows["t2"]], result)
        
    def testUpdateTableRowsFromMatchNeitherPlayedNorAwarded(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        tableRows = {}
        for tid in ["t1", "t2", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().updateTableRowsFromMatch(matchElement, tableRows)
        self.assertEquals(False, result)
        self.assertEquals(0, tableRows["t1"].played)
        self.assertEquals(0, tableRows["t2"].played)
        self.assertEquals(0, tableRows["t3"].played)
        
    def testUpdateTableRowsFromMatchAwarded(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <awardedMatch>
                <winner id="t2"/>
            </awardedMatch>
        </match>
        """
        tableRows = {}
        for tid in ["t1", "t2", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().updateTableRowsFromMatch(matchElement, tableRows)
        self.assertEquals(True, result)
        self.assertEquals(1, tableRows["t1"].played)
        self.assertEquals(1, tableRows["t2"].played)
        self.assertEquals(0, tableRows["t3"].played)
        
    def testUpdateTableRowsFromMatchPlayed(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <battingFirst>true</battingFirst>
                    <innings>
                        <runsScored>122</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <battingFirst>fals</battingFirst>
                    <innings>
                        <runsScored>103</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        tableRows = {}
        for tid in ["t1", "t2", "t3"]:
            tableRows[tid] = TableRow(tid, "")
        matchElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().updateTableRowsFromMatch(matchElement, tableRows)
        self.assertEquals(True, result)
        self.assertEquals(1, tableRows["t1"].played)
        self.assertEquals(1, tableRows["t2"].played)
        self.assertEquals(0, tableRows["t3"].played)
        
    def testCreateTableRows(self):
        xml = """
        <league>
            <team id="t1">
                <name>Rotherham</name>
            </team>
            <team id="t2">
                <name>Reading</name>
                <pointsDeduction>
                    <points>8</points>
                    <reason>Being a bit crap</reason>
                </pointsDeduction>
            </team>
            <team id="t3">
                <name>Charlton</name>
                <excludedFromTables/>
            </team>
            <team id="t4">
                <name>Oxford</name>
                <pointsDeduction>
                    <points>3</points>
                    <reason>Being very crap</reason>
                </pointsDeduction>
                <pointsDeduction>
                    <points>4</points>
                    <reason>Losing to Charlton</reason>
                </pointsDeduction>
            </team>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().createTableRows(leagueElement)
        expectedResults = {}
        expectedResults["t1"] = ["Rotherham"]
        expectedResults["t2"] = ["Reading", [8, "Being a bit crap"]] 
        expectedResults["t4"] = ["Oxford", [3, "Being very crap"], [4, "Losing to Charlton"]]
        self.assertEquals(len(expectedResults), len(result))
        for k in expectedResults.keys():
            tableRow = result[k]
            self.assertEquals(k, tableRow.teamId)
            exp = expectedResults[k]
            self.assertEquals(exp[0], tableRow.teamName)
            self.assertEquals(len(exp) - 1, len(tableRow.deductions))
            for i in range(1, len(exp)):
                ded = tableRow.deductions[i - 1]
                self.assertEquals(exp[i][0], ded.points)
                self.assertEquals(exp[i][1], ded.reason)
            
    def testGetLeagueTableNotAllGamesCompleteSomeToCome(self):
        xml = """
        <league>
            <name>The League</name>
            <teamsPromoted>2</teamsPromoted>
            <teamsRelegated>3</teamsRelegated>
            <team id="t1">
                <name>Rotherham</name>
            </team>
            <team id="t2">
                <name>Reading</name>
            </team>
            <team id="t3">
                <name>Charlton</name>
            </team>
            <team id="t4">
                <name>Oxford</name>
            </team>
            <match>
                <date>2013-08-06.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-07.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-08.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t1"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-09.18:15</date>
                <homeTeam id="t4"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t4"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-11.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-10.18:15</date>
                <homeTeam id="t2"/>
                <awayTeam id="t3"/>
                <awardedMatch>
                    <winner id="t2"/>
                </awardedMatch>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getLeagueTable(leagueElement)
        expectedResults = {}
        expectedResults["t1"] = [2, 0, ["t4"]]
        expectedResults["t2"] = [1, 2, []]
        expectedResults["t3"] = [0, 2, ["t4"]]
        expectedResults["t4"] = [1, 0, ["t1", "t3"]]
        self.assertEquals("The League", result.leagueName)
        self.assertEquals(2, result.promoted)
        self.assertEquals(3, result.relegated)
        self.assertEquals(datetime.date(2013, 8, 10), result.lastCompleteMatchDate)
        self.assertEquals(datetime.date(2013, 8, 11), result.lastScheduledMatchDate)
        self.assertEquals(1, result.toCome)
        self.assertEquals(len(expectedResults), len(result.tableRows))
        for k in expectedResults.keys():
            tableRow = result.tableRows[k]
            self.assertEquals(expectedResults[k][0], tableRow.won)
            self.assertEquals(expectedResults[k][1], tableRow.lost)
            self.assertEquals(sorted(expectedResults[k][2]), sorted(tableRow.remainingOpponents))
            
    def testGetLeagueTableNotAllGamesCompleteNoneToCome(self):
        xml = """
        <league>
            <name>The League</name>
            <teamsPromoted>2</teamsPromoted>
            <teamsRelegated>3</teamsRelegated>
            <team id="t1">
                <name>Rotherham</name>
            </team>
            <team id="t2">
                <name>Reading</name>
            </team>
            <team id="t3">
                <name>Charlton</name>
            </team>
            <team id="t4">
                <name>Oxford</name>
            </team>
            <match>
                <date>2013-08-06.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-15.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-08.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t1"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-09.18:15</date>
                <homeTeam id="t4"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t4"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-11.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-10.18:15</date>
                <homeTeam id="t2"/>
                <awayTeam id="t3"/>
                <awardedMatch>
                    <winner id="t2"/>
                </awardedMatch>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getLeagueTable(leagueElement)
        expectedResults = {}
        expectedResults["t1"] = [2, 0, ["t4"]]
        expectedResults["t2"] = [1, 2, []]
        expectedResults["t3"] = [0, 2, ["t4"]]
        expectedResults["t4"] = [1, 0, ["t1", "t3"]]
        self.assertEquals("The League", result.leagueName)
        self.assertEquals(2, result.promoted)
        self.assertEquals(3, result.relegated)
        self.assertEquals(datetime.date(2013, 8, 10), result.lastCompleteMatchDate)
        self.assertEquals(datetime.date(2013, 8, 15), result.lastScheduledMatchDate)
        self.assertEquals(0, result.toCome)
        self.assertEquals(len(expectedResults), len(result.tableRows))
        for k in expectedResults.keys():
            tableRow = result.tableRows[k]
            self.assertEquals(expectedResults[k][0], tableRow.won)
            self.assertEquals(expectedResults[k][1], tableRow.lost)
            self.assertEquals(sorted(expectedResults[k][2]), sorted(tableRow.remainingOpponents))
            
    def testGetLeagueTableAllGamesComplete(self):
        xml = """
        <league>
            <name>The League</name>
            <teamsPromoted>2</teamsPromoted>
            <teamsRelegated>1</teamsRelegated>
            <team id="t1">
                <name>Rotherham</name>
            </team>
            <team id="t2">
                <name>Reading</name>
            </team>
            <team id="t3">
                <name>Charlton</name>
            </team>
            <team id="t4">
                <name>Oxford</name>
            </team>
            <match>
                <date>2013-08-06.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-07.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t4"/>
                <awardedMatch>
                    <winner id="t4"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-08.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t1"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-09.18:15</date>
                <homeTeam id="t4"/>
                <awayTeam id="t2"/>
                <awardedMatch>
                    <winner id="t4"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-11.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t4"/>
                <awardedMatch>
                    <winner id="t1"/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-08-10.18:15</date>
                <homeTeam id="t2"/>
                <awayTeam id="t3"/>
                <awardedMatch>
                    <winner id="t2"/>
                </awardedMatch>
            </match>
            <tableNotes>Hello
            Goodbye
            </tableNotes>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getLeagueTable(leagueElement)
        expectedResults = {}
        expectedResults["t1"] = [3, 0, True, True, False]
        expectedResults["t4"] = [2, 1, False, True, False]
        expectedResults["t2"] = [1, 2, False, False, False]
        expectedResults["t3"] = [0, 3, False, False, True]
        self.assertEquals("The League", result.leagueName)
        self.assertEquals(2, result.promoted)
        self.assertEquals(1, result.relegated)
        self.assertEquals(datetime.date(2013, 8, 11), result.lastCompleteMatchDate)
        self.assertEquals(datetime.date(2013, 8, 11), result.lastScheduledMatchDate)
        self.assertEquals(0, result.toCome)
        self.assertEquals(len(expectedResults), len(result.tableRows))
        for k in expectedResults.keys():
            tableRow = result.tableRows[k]
            self.assertEquals(expectedResults[k][0], tableRow.won)
            self.assertEquals(expectedResults[k][1], tableRow.lost)
            self.assertEquals(expectedResults[k][2], tableRow.champions)
            self.assertEquals(expectedResults[k][3], tableRow.promoted)
            self.assertEquals(expectedResults[k][4], tableRow.relegated)
            self.assertEquals([], tableRow.remainingOpponents)
        self.assertEquals(["Hello", "Goodbye"], result.notes)
                        
    def testGetLeagueTableNoGamesComplete(self):
        xml = """
        <league>
            <name>The League</name>
            <teamsPromoted>2</teamsPromoted>
            <teamsRelegated>3</teamsRelegated>
            <team id="t1">
                <name>Rotherham</name>
            </team>
            <team id="t2">
                <name>Reading</name>
            </team>
            <team id="t3">
                <name>Charlton</name>
            </team>
            <team id="t4">
                <name>Oxford</name>
            </team>
            <match>
                <date>2013-08-06.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t2"/>
            </match>
            <match>
                <date>2013-08-07.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-08.18:15</date>
                <homeTeam id="t3"/>
                <awayTeam id="t1"/>
            </match>
            <match>
                <date>2013-08-09.18:15</date>
                <homeTeam id="t4"/>
                <awayTeam id="t2"/>
            </match>
            <match>
                <date>2013-08-11.18:15</date>
                <homeTeam id="t1"/>
                <awayTeam id="t4"/>
            </match>
            <match>
                <date>2013-08-10.18:15</date>
                <homeTeam id="t2"/>
                <awayTeam id="t3"/>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getLeagueTable(leagueElement)
        expectedResults = {}
        expectedResults["t1"] = [0, 0]
        expectedResults["t2"] = [0, 0]
        expectedResults["t3"] = [0, 0]
        expectedResults["t4"] = [0, 0]
        self.assertEquals("The League", result.leagueName)
        self.assertEquals(2, result.promoted)
        self.assertEquals(3, result.relegated)
        self.assertEquals(None, result.lastCompleteMatchDate)
        self.assertEquals(datetime.date(2013, 8, 11), result.lastScheduledMatchDate)
        self.assertEquals(0, result.toCome)
        self.assertEquals(len(expectedResults), len(result.tableRows))
        for k in expectedResults.keys():
            tableRow = result.tableRows[k]
            self.assertEquals(expectedResults[k][0], tableRow.won)
            self.assertEquals(expectedResults[k][1], tableRow.lost)
            
    def testGetLeagueReportNoLeagueSpecified(self):
        xml = """
        <model>
            <league id="l1">
                <name>League 1</name>
            </league>
            <league id="l2">
                <name>League 2</name>
            </league>
            <league id="l3">
                <name>League 3</name>
            </league>
            <league id="l4">
                <name>League 4</name>
            </league>
            <league id="l5">
                <name>League 5</name>
            </league>
            <league id="l6">
                <name>League 6</name>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getReport(rootElement, None)
        self.assertEqual(6, len(result.tables))
        
    def testGetLeagueReportLeagueSpecifiedButNotFound(self):
        xml = """
        <model>
            <league id="l1">
                <name>League 1</name>
            </league>
            <league id="l2">
                <name>League 2</name>
            </league>
            <league id="l3">
                <name>League 3</name>
            </league>
            <league id="l4">
                <name>League 4</name>
            </league>
            <league id="l5">
                <name>League 5</name>
            </league>
            <league id="l6">
                <name>League 6</name>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getReport(rootElement, "l7")
        self.assertEqual(0, len(result.tables))
        
    def testGetLeagueReportLeagueSpecifiedAndFound(self):
        xml = """
        <model>
            <league id="l1">
                <name>League 1</name>
            </league>
            <league id="l2">
                <name>League 2</name>
            </league>
            <league id="l3">
                <name>League 3</name>
            </league>
            <league id="l4">
                <name>League 4</name>
            </league>
            <league id="l5">
                <name>League 5</name>
            </league>
            <league id="l6">
                <name>League 6</name>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        result = LeagueTableReportGenerator().getReport(rootElement, "l3")
        self.assertEqual(1, len(result.tables))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCalculateBattingPointsScoreLessThan60NoWicketsPoints']
    unittest.main()