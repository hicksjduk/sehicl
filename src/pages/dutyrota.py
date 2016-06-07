'''
Created on 10 Sep 2013

@author: hicksj
'''
from pages.page import Page
from pages.pageLink import PageLink
import string

class DutyRota(Page):
    
    season = "2015/16"
    duties = []
    duties.append(("27th September", "Portsmouth &amp; Southsea"))
    duties.append(("4th October", "Locks Heath A"))
    duties.append(("11th October", "Petersfield"))
    duties.append(("18th October", "Sarisbury Athletic A"))
    duties.append(("25th October", "Sarisbury Athletic B"))
    duties.append(("1st November", "XIIth Men B"))
    duties.append(("8th November", "Waterlooville B"))
    duties.append(("15th November", "Portchester"))
    duties.append(("22nd November", "Havant A"))
    duties.append(("29th November", "Waterlooville A"))
    duties.append(("6th December", "ServiceMaster"))
    duties.append(("13th December", "IBM South Hants"))
    duties.append(("20th December", "Knowle Village"))
    duties.append(("3rd January", "Hambledon B"))
    duties.append(("10th January", "Portsmouth Academics"))
    duties.append(("17th January", "St James Casuals"))
    duties.append(("24th January", "Clanfield"))
    duties.append(("31st January", "Locks Heath B"))
    duties.append(("7th February", "XIIth Men A"))
    duties.append(("14th February", "IBM South Hants"))
    duties.append(("21st February", "Havant B"))
    duties.append(("28th February", "Southern Electric"))
    duties.append(("6th March", "Hambledon A"))
    duties.append(("13th March", "Purbrook"))
    
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