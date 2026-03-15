import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class BrokenLinkTests(BaseCase):
    @pytest.mark.owner('chenmei')
    @pytest.mark.priority('P3')
    @pytest.mark.description('验证检测页面链接中的损坏链接和 404 错误')
    def test_link_checking(self):
        self.open("https://seleniumbase.io/other/broken_page.html")
        print("\n(This test should fail)")
        self.assert_no_404_errors()
