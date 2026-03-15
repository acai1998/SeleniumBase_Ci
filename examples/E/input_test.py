from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class AngularMaterialInputTests(BaseCase):

    @pytest.mark.owner('zhaoliu')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test Angular Material input: entering invalid email shows validation error message')
    def test_invalid_input(self):
        # Test that there's an error for an invalid input
        self.open("https://material.angular.io/components/input/examples")
        self.type('input[type="email"]', "invalid")
        self.assert_element("mat-error")

    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test Angular Material input: valid email address does not trigger validation error')
    def test_valid_email_input(self):
        self.open("https://material.angular.io/components/input/examples")
        email_input = 'input[type="email"]'
        self.type(email_input, "test@example.com")
        # No error should appear for valid email
        self.assert_element_not_visible("mat-error")

    @pytest.mark.owner('zhaoliu')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test Angular Material input: clearing the field resets value to empty string')
    def test_clear_input(self):
        self.open("https://material.angular.io/components/input/examples")
        email_input = 'input[type="email"]'
        self.type(email_input, "test@example.com")
        self.assert_attribute(email_input, "value", "test@example.com")
        self.clear(email_input)
        self.assert_attribute(email_input, "value", "")
