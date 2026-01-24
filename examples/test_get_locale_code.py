from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class LocaleTests(BaseCase):
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test get locale code')
    def test_get_locale_code(self):
        self.open("about:blank")
        locale_code = self.get_locale_code()
        message = '\nLocale Code = "%s"' % locale_code
        print(message)
        self.set_messenger_theme(theme="flat", location="top_center")
        self.post_message(message, duration=4)
