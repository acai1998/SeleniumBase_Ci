from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class MultipleDriversTest(BaseCase):
    @pytest.mark.owner('zhaoliu')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证同时使用多个 WebDriver 实例')
    def test_multiple_drivers(self):
        if self.browser == "safari":
            self.open_if_not_url("about:blank")
            print("\n  Safari doesn't support multiple drivers.")
            self.skip("Safari doesn't support multiple drivers.")
        self.open("data:text/html,<h1>Driver 1</h1>")
        driver2 = self.get_new_driver()
        self.open("data:text/html,<h1>Driver 2</h1>")
        self.switch_to_default_driver()  # Driver 1
        self.highlight("h1")
        self.assert_text("Driver 1", "h1")
        self.switch_to_driver(driver2)  # Driver 2
        self.highlight("h1")
        self.assert_text("Driver 2", "h1")
