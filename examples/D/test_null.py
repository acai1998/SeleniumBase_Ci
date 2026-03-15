from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class NullTests(BaseCase):
    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P1')
    @pytest.mark.description('验证空值和无效输入的处理')
    def test_null(self):
        pass
