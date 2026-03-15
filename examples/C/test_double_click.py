"""Test double_click() after switching into iframes."""
from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class DoubleClickTests(BaseCase):
    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证切换到 Frame 并执行双击操作')
    def test_switch_to_frame_and_double_click(self):
        self.open("https://seleniumbase.io/w3schools/double_click")
        self.assert_title("Double Click Testing")
        self.click("button#runbtn")
        self.switch_to_frame("iframe#iframeResult")
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")

    @pytest.mark.owner('wubin')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test switch to frame of element and double click')
    def test_switch_to_frame_of_element_and_double_click(self):
        self.open("https://seleniumbase.io/w3schools/double_click")
        self.assert_title("Double Click Testing")
        self.click("button#runbtn")
        self.switch_to_frame_of_element('[ondblclick="myFunction()"]')
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")
