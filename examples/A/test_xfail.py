"""Testing the @pytest.mark.xfail marker.
https://docs.pytest.org/en/latest/skipping.html
(The test is expected to fail, but don't fail the entire build for it.)"""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class XFailTests(BaseCase):
    @pytest.mark.xfail
    @pytest.mark.owner('lisi')
    @pytest.mark.priority('P1')
    @pytest.mark.description('验证 pytest xfail 标记正确标记已知失败用例')
    def test_xfail(self):
        self.open("https://xkcd.com/376/")
        self.sleep(1)  # Time to read the comic
        self.fail("There is a known bug here!")
