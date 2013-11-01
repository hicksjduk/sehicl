'''
Created on 10 Sep 2013

@author: hicksj
'''
from pages.page import Page
from pages.pageLink import PageLink
import string

class DutyRota(Page):
    
    season = "2013/14"
    duties = []
    duties.append(("6th October", "Waterlooville B"))
    duties.append(("13th October", "Havant A"))
    duties.append(("20th October", "United Services"))
    duties.append(("27th October", "Portsmouth Post Office"))
    duties.append(("3rd November", "Knowle Village"))
    duties.append(("10th November", "Purbrook A"))
    duties.append(("24th November", "Portchester"))
    duties.append(("1st December", "Petersfield"))
    duties.append(("8th December", "Southern Electric"))
    duties.append(("15th December", "XIIth Men B"))
    duties.append(("22nd December", "Sarisbury Athletic A"))
    duties.append(("5th January", "Hambledon B"))
    duties.append(("12th January", "Portsmouth Priory"))
    duties.append(("19th January", "Sarisbury Athletic B"))
    duties.append(("26th January", "Purbrook B"))
    duties.append(("2nd February", "Waterlooville A"))
    duties.append(("9th February", "Hambledon A"))
    duties.append(("16th February", "XIIth Men A"))
    duties.append(("23rd February", "Railway Triangle"))
    duties.append(("2nd March", "Havant B"))
    duties.append(("9th March", "Portsmouth & Southsea"))
    duties.append(("16th March", "Sarisbury Athletic A"))
    duties.append(("23rd March", "Petersfield"))
    
    def __init__(self, pageId):
        Page.__init__(self, pageId)
        
    def getTitle(self):
        return "SEHICL Duty Rota"
    
    def getContent(self):
        html = """
        <h1>Duty team rota {season}</h1>
        <p>
            <a href="{rules.url}#sectionT">Article T</a> of the League's rules states
            that the designated duty team for each evening must attend and operate
            the manual scoreboards for all senior games on that evening.
        </p>
        {duties}
        """
        answer = html.format(season=self.season, rules=PageLink("rules", self), duties=self.getDutyData())
        return answer
    
    def getDutyData(self):
        if len(self.duties) == 0:
            answer = "<p>The duty rota will be available shortly.</p>"
        else:
            html = """
            <table id="dutyrota">
                <tbody>
                    {items}
                </tbody>
            </table>
            """
            answer = html.format(items=string.join(self.getDutyItems(), "\n"))
        return answer
        
    def getDutyItems(self):
        html = """
        <tr>
            <td class="datecol">{date}</td>
            <td class="teamcol">{team}</td>
        </tr>
        """
        answer = []
        for k, v in self.duties:
            answer.append(html.format(date=k, team=v))
        return answer