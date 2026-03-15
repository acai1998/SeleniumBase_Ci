import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CheckboxTests(BaseCase):
    @pytest.mark.owner('zhangsan')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test checkbox selection and radio button interactions on W3Schools examples')
    def test_checkboxes_and_radio_buttons(self):
        self.open("https://seleniumbase.io/w3schools/checkboxes")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")
        checkbox = "input#vehicle2"
        self.assert_false(self.is_selected(checkbox))
        self.click(checkbox)
        self.assert_true(self.is_selected(checkbox))
        self.open("https://seleniumbase.io/w3schools/radio_buttons")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")
        option_button = "input#css"
        self.assert_false(self.is_selected(option_button))
        self.click(option_button)
        self.assert_true(self.is_selected(option_button))
