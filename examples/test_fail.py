""" This test fails on purpose to demonstrate
    the logging capabilities of SeleniumBase.
    >>> pytest test_fail.py --html=report.html
    This creates ``report.html`` with details.
    (Also find log files in ``latest_logs/``)"""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class FailingTests(BaseCase):
    @pytest.mark.expected_failure
    @pytest.mark.owner('liuyang')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test expected failure: army of robots not found on XKCD desert island comic')
    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        print("\n(This test should fail)")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)
