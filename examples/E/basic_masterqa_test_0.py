from seleniumbase import MasterQA
import pytest
MasterQA.main(__name__, __file__)


class MasterQATests(MasterQA):
    
    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P3')
    @pytest.mark.description('验证 MasterQA 手动验证流程：页面导航和视觉问题确认')
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
