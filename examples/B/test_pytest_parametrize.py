import pytest


@pytest.mark.parametrize(
    "value", ["List of Features", "Command Line Options"]
)
@pytest.mark.owner('zhouqiang')
@pytest.mark.priority('P1')
@pytest.mark.description('Test SeleniumBase sb fixture with pytest parametrize in a standalone function')
def test_sb_fixture_with_no_class(sb, value):
    sb.open("seleniumbase.io/help_docs/install/")
    sb.type('input[aria-label="Search"]', value)
    sb.click("nav h1 mark")
    sb.assert_title_contains(value)
    sb.assert_text(value, "div.md-content")


class Test_SB_Fixture:
    @pytest.mark.parametrize(
        "value", ["Console Scripts", "API Reference"]
    )
    @pytest.mark.owner('zhangsan')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test SeleniumBase sb fixture with pytest parametrize inside a test class')
    def test_sb_fixture_inside_class(self, sb, value):
        sb.open("seleniumbase.io/help_docs/install/")
        sb.type('input[aria-label="Search"]', value)
        sb.click("nav h1 mark")
        sb.assert_title_contains(value)
        sb.assert_text(value, "div.md-content")
