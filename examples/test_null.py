from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class NullTests(BaseCase):
    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test opening a blank page and asserting no elements are present as baseline')
    def test_null(self):
        pass
