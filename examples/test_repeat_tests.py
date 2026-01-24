""" Tests to demonstrate how to repeat the same test multiple times.
    The 1st example uses the "parameterized" library.
    The 2nd example uses "pytest.mark.parametrize()". (NO class)
    The 3rd example uses "pytest.mark.parametrize()". (in class) """
import pytest
from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "-n6")

url = "data:text/html,<h2>Hello</h2><p><input />&nbsp;<button>OK!</button></p>"


class RepeatTests(BaseCase):
    @parameterized.expand([[]] * 2)
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test repeat this test with parameterized')
    def test_repeat_this_test_with_parameterized(self):
        self.open(url)
        self.type("input", "SeleniumBase is fun")
        self.click('button:contains("OK!")')
        self.assert_text("Hello", "h2")


@pytest.mark.parametrize("", [[]] * 2)
@pytest.mark.owner('caijinwei')
@pytest.mark.priority('P2')
@pytest.mark.description('Test repeat this test with pytest parametrize')
def test_repeat_this_test_with_pytest_parametrize(sb):
    sb.open(url)
    sb.type("input", "SeleniumBase is fun")
    sb.click('button:contains("OK!")')
    sb.assert_text("Hello", "h2")


class RepeatTestsWithPytest:
    @pytest.mark.parametrize("", [[]] * 2)
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test repeat test with pytest parametrize')
    def test_repeat_test_with_pytest_parametrize(self, sb):
        sb.open(url)
        sb.type("input", "SeleniumBase is fun")
        sb.click('button:contains("OK!")')
        sb.assert_text("Hello", "h2")
