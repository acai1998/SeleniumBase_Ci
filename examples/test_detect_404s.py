import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class BrokenLinkTests(BaseCase):
    @pytest.mark.owner('chenmei')
    @pytest.mark.priority('P3')
    @pytest.mark.description('Test all page links to detect broken links and 404 errors')
    def test_link_checking(self):
        self.open("https://seleniumbase.io/other/broken_page.html")
        print("\n(This test should fail)")
        self.assert_no_404_errors()
