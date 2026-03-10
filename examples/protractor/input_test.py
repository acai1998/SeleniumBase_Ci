from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class AngularMaterialInputTests(BaseCase):
    
    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test Angular Material input functionality - enter invalid input and verify error message')
    def test_invalid_input(self):
        # Test that there's an error for an invalid input
        self.open("https://material.angular.io/components/input/examples")
        self.type('input[type="email"]', "invalid")
        self.assert_element("mat-error")
