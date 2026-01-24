from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class URLTestClass(BaseCase):
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test URL asserts functionality')
    def test_url_asserts(self):
        self.open("https://seleniumbase.io/help_docs/how_it_works/")
        self.assert_url("https://seleniumbase.io/help_docs/how_it_works/")
        self.assert_title_contains("How it Works")
        self.js_click('nav a:contains("Coffee Cart")')
        self.assert_url_contains("/coffee")
        self.assert_title("Coffee Cart")
