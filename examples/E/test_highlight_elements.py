from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class HighlightTest(BaseCase):
    @pytest.mark.owner('zhangsan')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证表单输入框的高亮显示功能')
    def test_highlight_inputs(self):
        self.open("https://seleniumbase.io/demo_page")
        if self.headed:
            self.highlight_elements("input", loops=2)  # Default: 4
        else:
            self.highlight_elements("input", loops=1, limit=3)
