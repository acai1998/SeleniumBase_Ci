from seleniumbase import MasterQA
import pytest
MasterQA.main(__name__, __file__)


class MasterQATests(MasterQA):
    
    @pytest.mark.owner('wangwu')
        @pytest.mark.priority('P3')
        @pytest.mark.description('Test MasterQA manual verification flow: navigate pages and confirm visual questions')
    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P3')
    @pytest.mark.description('Test MasterQA manual verification flow: navigate pages and confirm visual questions')
    def test_masterqa(self):
        self.open("https://seleniumbase.io/devices/")
        self.highlight("div.mockup-wrapper")
        self.verify("Do you see 4 computer devices?")
        self.open("https://seleniumbase.io/demo_page")
        self.highlight("table")
        self.verify("Do you see elements in a table?")
        self.open("https://xkcd.com/1700/")
        self.highlight("#comic")
        self.verify("Do you see a webcomic?")
