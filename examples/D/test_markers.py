""" These tests demonstrate pytest marker use for finding and running tests.

    Usage examples from this file:
        pytest -v -m marker_test_suite                 # Runs A, B, C, D
        pytest -v -m marker1                           # Runs A
        pytest -v -m marker2                           # Runs B, C
        pytest -v -m marker3                           # Runs C
        pytest test_markers.py -v -m "not marker2"     # Runs A, D

    (The "-v" will display the names of tests as they run.)
    (Add "--collect-only" to display names of tests without running them.)"""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


@pytest.mark.marker_test_suite
class MarkerTestSuite(BaseCase):
    @pytest.mark.marker1
    @pytest.mark.owner('liuyang')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test A')
    def test_A(self):
        self.open("https://xkcd.com/1319/")
        self.assert_text("Automation", "div#ctitle")

    @pytest.mark.marker2
    @pytest.mark.owner('wubin')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test B')
    def test_B(self):
        self.open("https://www.xkcd.com/1700/")
        self.assert_text("New Bug", "div#ctitle")

    @pytest.mark.marker2
    @pytest.mark.marker3  # Tests can have multiple markers
    @pytest.mark.owner('lisi')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test C')
    def test_C(self):
        self.open("https://xkcd.com/844/")
        self.assert_text("Good Code", "div#ctitle")

    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test D')
    def test_D(self):
        self.open("https://xkcd.com/2021/")
        self.assert_text("Software Development", "div#ctitle")
