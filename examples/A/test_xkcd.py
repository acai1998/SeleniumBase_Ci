from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    @pytest.mark.owner('zhaoliu')
    @pytest.mark.priority('P3')
    @pytest.mark.description('验证 XKCD 漫画网站导航和 MasterQA 视觉验证')
    def test_xkcd(self):
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click_link("About")
        self.assert_exact_text("xkcd.com", "h2")
        self.click_link("comic #249")
        self.assert_element('img[alt*="Chess"]')
