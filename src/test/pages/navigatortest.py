'''
Created on 15 Aug 2013

@author: hicksj
'''
from test.testbase import TestBase
import unittest
from pages.navigatoritem import NavigatorItem
from pages.page import Page
from xml.etree import ElementTree
from pages.navigator import Navigator


class Test(TestBase):
    
    def testIsSelectedItemHasNoPageIdNoParamsPageHasNoIdNoParams(self):
        item = NavigatorItem(url="http://sehicl.org.uk")
        page = self.getPage(None)
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasNoIdNoParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage(None)
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasNoIdNoParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage(None)
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasNoPageIdNoParamsPageHasIdNoParams(self):
        item = NavigatorItem(url="http://sehicl.org.uk")
        page = self.getPage("hello")
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasDifferentIdNoParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage("hej")
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasDifferentIdNoParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hej")
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasSameIdNoParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage("hello")
        result = item.isSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasSameIdNoParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hello")
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasNoPageIdNoParamsPageHasNoIdAndParams(self):
        item = NavigatorItem(url="http://sehicl.org.uk")
        page = self.getPage(None, {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasNoIdAndParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage(None, {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasNoIdAndParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage(None, {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasNoPageIdNoParamsPageHasIdAndParams(self):
        item = NavigatorItem(url="http://sehicl.org.uk")
        page = self.getPage("hello", {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasDifferentIdAndParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage("hej", {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasDifferentIdAndParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hej", {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdNoParamsPageHasSameIdAndParams(self):
        item = NavigatorItem(pageId="hello")
        page = self.getPage("hello", {"param": "param"})
        result = item.isSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasSameIdAndDifferentParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hello", {"param": "param"})
        result = item.isSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testIsSelectedItemHasPageIdAndParamsPageHasSameIdAndExtraParams(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.isSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)
        
    def getPage(self, pageId, params={}):
        answer = Page(pageId)
        answer.allParams = params
        return answer
        
    def testContainsSelectedItemIsSelected(self):
        item = NavigatorItem(pageId="hello", params={"text": "bonjour"})
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasNoIdAndHasNoItems(self):
        item = NavigatorItem(pageId="sagsd", params={"text": "bonjour"})
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasAnIdThatDoesNotMatchPageAndHasNoItems(self):
        item = NavigatorItem(itemId="fixtures", pageId="sagsd", params={"text": "bonjour"})
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasAnIdThatMatchesPage(self):
        item = NavigatorItem(itemId="fixtures", pageId="sagsd", params={"text": "bonjour"})
        page = self.getPage("leagueFixtures", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasNoIdAndHasNoMatchingItems(self):
        items = [NavigatorItem(pageId="asfsdf"), NavigatorItem(pageId="aaaaa")]
        item = NavigatorItem(pageId="sagsd", params={"text": "bonjour"}, items=items)
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasAnIdThatDoesNotMatchPageAndHasNoMatchingItems(self):
        items = [NavigatorItem(pageId="asfsdf"), NavigatorItem(pageId="aaaaa")]
        item = NavigatorItem(itemId="fixtures", pageId="sagsd", params={"text": "bonjour"}, items=items)
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasNoIdAndHasAMatchingItem(self):
        items = [NavigatorItem(pageId="asfsdf"), NavigatorItem(pageId="hello"), NavigatorItem(pageId="aaaaa")]
        item = NavigatorItem(pageId="sagsd", params={"text": "bonjour"}, items=items)
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testContainsSelectedItemIsNotSelectedAndHasAnIdThatDoesNotMatchPageAndHasAMatchingItem(self):
        items = [NavigatorItem(pageId="asfsdf"), NavigatorItem(pageId="aaaaa"), NavigatorItem("hello")]
        item = NavigatorItem(itemId="fixtures", pageId="sagsd", params={"text": "bonjour"}, items=items)
        page = self.getPage("hello", {"param": "param", "text": "bonjour"})
        result = item.containsSelected(page)
        expectedResult = True
        self.assertEqual(expectedResult, result)

    def testGetItemLinkItemIsCurrent(self):
        item = NavigatorItem(pageId="hello", text="Home")
        page = self.getPage("hello")
        result = item.getItemLink(page)
        expectedResult = """
        <span class="current">Home</span>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetItemLinkItemIsNotCurrentNoSession(self):
        item = NavigatorItem(pageId="hello", text="Home")
        page = self.getPage("goodbye")
        result = item.getItemLink(page)
        expectedResult = """
        <a href="/cgi-bin/page.py?id=hello">Home</a>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetItemLinkItemIsNotCurrentWithSession(self):
        item = NavigatorItem(pageId="hello", text="Home", params={"hello": 0})
        page = self.getPage("goodbye", {"session": 53436})
        result = item.getItemLink(page)
        expectedResult = """
        <a href="/cgi-bin/page.py?id=hello&session=53436&hello=0">Home</a>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetItemLinkItemIsNotCurrentUrlIsSpecified(self):
        item = NavigatorItem(url="http://sehicl.org.uk", text="Home")
        page = self.getPage("goodbye", {"session": 53436})
        result = item.getItemLink(page)
        expectedResult = """
        <a href="http://sehicl.org.uk" target="_blank">Home</a>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHtmlItemIsNotCurrentHasNoContainedItemsNoSession(self):
        item = NavigatorItem(pageId="hello", text="Hello", params={"hello": 0})
        page = self.getPage("afaasfsa")
        result = item.getHtml(page)
        expectedResult = """
        <li>
            <a href="/cgi-bin/page.py?id=hello&hello=0">Hello</a>
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetHtmlItemIsCurrentHasNoContainedItems(self):
        item = NavigatorItem(pageId="hello", text="Hello", params={"hello": 0})
        page = self.getPage("hello", {"hello": 0})
        result = item.getHtml(page)
        expectedResult = """
        <li>
            <span class="current">Hello</span>
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetHtmlItemHasContainedItemsIsSelected(self):
        subItems = []
        subItems.append(NavigatorItem(pageId="aasda", text="Item1"))
        subItems.append(NavigatorItem(pageId="aadsgasgas", text="Item2"))
        item = NavigatorItem(pageId="aadgas", text="Hello", params={"hello": 0}, items=subItems)
        page = self.getPage("aadgas", params={"hello": 0, "session": "12412"})
        result = item.getHtml(page)
        expectedResult = """
        <li>
            <span class="current">Hello</span>
            <ul id="currentMenu">
                <li>
                    <a href="/cgi-bin/page.py?id=aasda&session=12412">Item1</a>
                </li>
                <li>
                    <a href="/cgi-bin/page.py?id=aadsgasgas&session=12412">Item2</a>
                </li>
            </ul>
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetHtmlItemHasContainedItemsIncludesSelected(self):
        subSubItem = NavigatorItem(pageId="asdgasgsa", text="Sub-sub-item")
        subItems = []
        subItems.append(NavigatorItem(pageId="aasaassasa", text="Sub-item 1", items=[subSubItem]))
        subItems.append(NavigatorItem(pageId="asasdasfa", text="Sub-item 2"))
        item = NavigatorItem(pageId="hello", text="Hello", params={"hello": 0}, items=subItems)
        page = self.getPage("asdgasgsa", {"session": "12412"})
        result = item.getHtml(page)
        expectedResult = """
        <li>
            <a href="/cgi-bin/page.py?id=hello&session=12412&hello=0">Hello</a>
            <ul id="currentMenu">
                <li>
                    <a href="/cgi-bin/page.py?id=aasaassasa&session=12412">Sub-item 1</a>
                    <ul id="currentMenu">
                        <li>
                            <span class="current">Sub-sub-item</span>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="/cgi-bin/page.py?id=asasdasfa&session=12412">Sub-item 2</a>
                </li>
            </ul>
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetItemNoPageNoTextNoParamsNoUrlNoSubItems(self):
        xml = """
        <item/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageNoTextNoParamsNoUrlNoSubItems(self):
        xml = """
        <item pageId="hello"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageTextNoParamsNoUrlNoSubItems(self):
        xml = """
        <item>A page</item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageTextNoParamsNoUrlNoSubItems(self):
        xml = """
        <item pageId="hello">
            Another page
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageNoTextParamsNoUrlNoSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageNoTextParamsNoUrlNoSubItems(self):
        xml = """
        <item pageId="hello" name="Rachel" surname="Hicks"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Rachel", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageTextParamsNoUrlNoSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks">A page</item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageTextParamsNoUrlNoSubItems(self):
        xml = """
        <item pageId="hello" name="Jeremy" surname="Hicks">
            Another page
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageNoTextNoParamsUrlNoSubItems(self):
        xml = """
        <item url="aafafs"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageNoTextNoParamsUrlNoSubItems(self):
        xml = """
        <item pageId="hello" url="aafafs"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageTextNoParamsUrlNoSubItems(self):
        xml = """
        <item url="aafafs">A page</item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageTextNoParamsUrlNoSubItems(self):
        xml = """
        <item pageId="hello" url="aafafs">
            Another page
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageNoTextParamsUrlNoSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks" url="aafafs"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageNoTextParamsUrlNoSubItems(self):
        xml = """
        <item pageId="hello" name="Rachel" surname="Hicks" url="aafafs"/>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Rachel", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageTextParamsUrlNoSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks" url="aafafs">A page</item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemPageTextParamsUrlNoSubItems(self):
        xml = """
        <item pageId="hello" name="Jeremy" surname="Hicks" url="aafafs">
            Another page
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(0, len(result.items))

    def testGetItemNoPageNoTextNoParamsNoUrlSubItems(self):
        xml = """
        <item>
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageNoTextNoParamsNoUrlSubItems(self):
        xml = """
        <item pageId="hello">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageTextNoParamsNoUrlSubItems(self):
        xml = """
        <item>A page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageTextNoParamsNoUrlSubItems(self):
        xml = """
        <item pageId="hello">
            Another page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageNoTextParamsNoUrlSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageNoTextParamsNoUrlSubItems(self):
        xml = """
        <item pageId="hello" name="Rachel" surname="Hicks">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Rachel", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageTextParamsNoUrlSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks">A page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageTextParamsNoUrlSubItems(self):
        xml = """
        <item pageId="hello" name="Jeremy" surname="Hicks">
            Another page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual(None, result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageNoTextNoParamsUrlSubItems(self):
        xml = """
        <item url="aafafs">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageNoTextNoParamsUrlSubItems(self):
        xml = """
        <item pageId="hello" url="aafafs">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageTextNoParamsUrlSubItems(self):
        xml = """
        <item url="aafafs">A page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageTextNoParamsUrlSubItems(self):
        xml = """
        <item pageId="hello" url="aafafs">
            Another page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageNoTextParamsUrlSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks" url="aafafs">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual(None, result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageNoTextParamsUrlSubItems(self):
        xml = """
        <item pageId="hello" name="Rachel" surname="Hicks" url="aafafs">
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Hello", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Rachel", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemNoPageTextParamsUrlSubItems(self):
        xml = """
        <item name="Jeremy" surname="Hicks" url="aafafs">A page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual(None, result.pageId)
        self.assertEqual("A page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetItemPageTextParamsUrlSubItems(self):
        xml = """
        <item pageId="hello" name="Jeremy" surname="Hicks" url="aafafs">
            Another page
            <item pageId="1"/>
            <item pageId="2"/>
            <item pageId="3"/>
        </item>
        """
        element = ElementTree.fromstring(xml)
        result = Navigator().getItem(element)
        self.assertEqual("hello", result.pageId)
        self.assertEqual("Another page", result.text)
        self.assertEqual("aafafs", result.url)
        self.assertEqual({"name": "Jeremy", "surname": "Hicks"}, result.pageParams)
        self.assertEqual(3, len(result.items))

    def testGetHtml(self):
        xml = """
        <navigator>
            <item pageId="hello" name="Jeremy" surname="Hicks" url="aafafs">
                Another page
                <item pageId="1">Item 1</item>
                <item pageId="2">Item 2</item>
                <item pageId="3">Item 3</item>
            </item>
            <item pageId="goodbye">Goodbye</item>
        </navigator>
        """
        page = self.getPage("1", {"session": 123})
        result = Navigator(xml).getHtml(page)
        expectedResult = """
        <ul class="navigator">
            <li>
                <a href="aafafs" target="_blank">Another page</a>
                <ul id="currentMenu">
                    <li>
                        <span class="current">Item 1</span>
                    </li>
                    <li>
                        <a href="/cgi-bin/page.py?id=2&session=123">Item 2</a>
                    </li>
                    <li>
                        <a href="/cgi-bin/page.py?id=3&session=123">Item 3</a>
                    </li>
                </ul>
            </li>
            <li>
                <a href="/cgi-bin/page.py?id=goodbye&session=123">Goodbye</a>
            </li>
        </ul>
        """
        self.assertMultiLineEqual(expectedResult, result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsSelectedItemHasNoPagePageDefHasNoPage']
    unittest.main()