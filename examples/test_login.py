"""A SeleniumBase test for verifying Login functionality on Swag Labs."""
from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class SwagLabsLoginTests(BaseCase):
    def login_to_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.wait_for_element("div.login_logo")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test login and logout functionality on Swag Labs')
    def test_swag_labs_login(self):
        self.login_to_swag_labs()
        self.assert_element("div.inventory_list")
        self.assert_element('.inventory_item:contains("Backpack")')
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")
