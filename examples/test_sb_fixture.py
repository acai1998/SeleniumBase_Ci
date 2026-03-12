import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


# "sb" pytest fixture test in a method with no class
@pytest.mark.owner('zhouqiang')
@pytest.mark.priority('P1')
@pytest.mark.description('Test SeleniumBase sb fixture with pytest parametrize in a standalone function')
def test_sb_fixture_with_no_class(sb: BaseCase):
    sb.open("seleniumbase.io/help_docs/install/")
    sb.type('input[aria-label="Search"]', "GUI Commander")
    sb.click('mark:contains("Commander")')
    sb.assert_title_contains("GUI / Commander")


# "sb" pytest fixture test in a method inside a class
class Test_SB_Fixture:
    @pytest.mark.owner('zhangsan')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test SeleniumBase sb fixture with pytest parametrize inside a test class')
    def test_sb_fixture_inside_class(self, sb: BaseCase):
        sb.open("seleniumbase.io/help_docs/install/")
        sb.type('input[aria-label="Search"]', "GUI Commander")
        sb.click('mark:contains("Commander")')
        sb.assert_title_contains("GUI / Commander")
