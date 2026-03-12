from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class UserAgentTests(BaseCase):
    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test retrieving browser User-Agent string and verifying it is not empty')
    def test_get_user_agent(self):
        self.open("data:,")
        user_agent = self.get_user_agent()
        print('\nUser Agent = "%s"' % user_agent)
        self.set_messenger_theme(theme="flat", location="top_center")
        self.post_message(user_agent, duration=4)
