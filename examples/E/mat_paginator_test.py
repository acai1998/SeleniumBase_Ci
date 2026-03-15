from seleniumbase import BaseCase
import pytest
BaseCase.main(__name__, __file__)


class AngularMaterialPaginatorTests(BaseCase):
    @pytest.mark.owner('wubin')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test Angular Material paginator: navigate next/previous pages and verify page range label')
    def test_pagination(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.click_if_visible("button.mat-mdc-button")
        self.scroll_to("div.mat-mdc-paginator-page-size")
        # Set pagination to 5 items per page
        self.click("mat-select > div")
        self.click("mat-option:nth-of-type(1)")
        # Verify navigation to the next page
        self.click('button[aria-label="Next page"]')
        self.assert_exact_text(
            "6 – 10 of 50", ".mat-mdc-paginator-range-label"
        )
        # Verify navigation to the previous page
        self.click('button[aria-label="Previous page"]')
        self.assert_exact_text(
            "1 – 5 of 50", ".mat-mdc-paginator-range-label"
        )
        # Set pagination to 10 items per page
        self.click("mat-select > div")
        self.click("mat-option:nth-of-type(2)")
        # Verify page with correct number of pages
        self.assert_exact_text(
            "1 – 10 of 50", ".mat-mdc-paginator-range-label"
        )

    @pytest.mark.owner('zhouqiang')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test Angular Material paginator: navigate to last page and verify final range label')
    def test_pagination_last_page(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.click_if_visible("button.mat-mdc-button")
        self.scroll_to("div.mat-mdc-paginator-page-size")
        # Navigate to last page by clicking next multiple times
        for i in range(9):
            self.click('button[aria-label="Next page"]')
        self.assert_exact_text("46 – 50 of 50", ".mat-mdc-paginator-range-label")

    @pytest.mark.owner('zhaoliu')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test Angular Material paginator: dropdown shows available page size options')
    def test_pagination_page_size_options(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.click_if_visible("button.mat-mdc-button")
        self.scroll_to("div.mat-mdc-paginator-page-size")
        # Open page size dropdown and verify options
        self.click("mat-select > div")
        self.assert_element("mat-option:nth-of-type(1)")
        self.assert_element("mat-option:nth-of-type(2)")
