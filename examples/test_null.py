from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class NullTests(BaseCase):
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test null placeholder')
    def test_null(self):
        pass
