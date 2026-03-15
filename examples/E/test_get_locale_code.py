from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class LocaleTests(BaseCase):
    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P2')
    @pytest.mark.description('验证获取本地化语言代码的功能')
    def test_get_locale_code(self):
        self.open("about:blank")
        locale_code = self.get_locale_code()
        message = '\nLocale Code = "%s"' % locale_code
        print(message)
        self.set_messenger_theme(theme="flat", location="top_center")
        self.post_message(message, duration=4)
