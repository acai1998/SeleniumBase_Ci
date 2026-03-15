"""Assert that multiple elements are present or visible:
HTML Presence: assert_elements_present()
HTML Visibility: assert_elements() <> assert_elements_visible()"""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ListAssertTest(BaseCase):
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证列表元素断言方法的准确性')
    def test_assert_list_of_elements(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_elements_present("head", "style", "script")
        self.assert_elements("h1", "h2", "h3")
        my_list = ["#myDropdown", "#myButton", "#mySlider"]
        self.assert_elements(my_list)
