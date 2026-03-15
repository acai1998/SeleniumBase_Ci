"""TAG:contains("TEXT") is a special, non-standard CSS Selector
that gets converted to XPath: '//TAG[contains(., "TEXT")]'
before it's used by Selenium calls. Also part of jQuery."""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ContainsSelectorTests(BaseCase):
    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证 CSS 包含选择器的正确工作')
    def test_contains_selector(self):
        self.open("https://xkcd.com/2207/")
        self.assert_element('div.box div:contains("Math Work")')
        self.click('a:contains("Next")')
        self.assert_element('div div:contains("Drone Fishing")')
