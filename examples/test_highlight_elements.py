from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class HighlightTest(BaseCase):
    @pytest.mark.owner('chenmei')
    @pytest.mark.priority('P3')
    @pytest.mark.description('Test highlight inputs')
    def test_highlight_inputs(self):
        self.open("https://seleniumbase.io/demo_page")
        if self.headed:
            self.highlight_elements("input", loops=2)  # Default: 4
        else:
            self.highlight_elements("input", loops=1, limit=3)
