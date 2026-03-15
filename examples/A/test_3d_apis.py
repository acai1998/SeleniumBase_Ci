import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--enable-3d-apis")


class ThreeJSTest(BaseCase):

    @pytest.mark.owner('liuyang')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证 Three.js 3D 动画在 WebGL 上的渲染效果')
    def test_animation(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            self.skip("Skip this test in headless mode!")
        if self.is_chromium() and not self.enable_3d_apis:
            self.get_new_driver(enable_3d_apis=True)  # --enable-3d-apis
        url = "https://threejs.org/examples/#webgl_animation_skinning_morph"
        self.open(url)
        self.switch_to_frame("iframe#viewer")
        self.sleep(0.8)
        self.click('button:contains("Wave")')
        self.sleep(3)

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证导航链接跳转到咖啡购物页面')
    def test_1_verify_nav_link_to_coffee_cart(self):
        self.open("https://seleniumbase.io/help_docs/customizing_test_runs/")
        self.js_click('nav a:contains("Coffee Cart")')
        self.assert_title("Coffee Cart")
        self.assert_element('h4:contains("Espresso")')

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证购买单个卡布奇诺咖啡的完整流程')
    def test_buy_one_cappuccino(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-test="Cappuccino"]')
        self.assert_exact_text("cart (1)", 'a[aria-label="Cart page"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $19.00", 'button[data-test="checkout"]')
        self.click('button[data-test="checkout"]')
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", 'button[data-test="checkout"]')

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('测试用例说明')
    @parameterized.expand([[False], [True]])
    def test_coffee_promo_with_preview(self, accept_promo):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-test="Espresso"]')
        self.click('div[data-test="Americano"]')
        self.click('div[data-test="Cafe_Latte"]')
        self.assert_exact_text("cart (3)", 'a[aria-label="Cart page"]')
        promo = False
        total_string = "Total: $33.00"
        if self.is_element_visible("div.promo"):
            self.assert_text("Get an extra cup of Mocha for $4.", "div.promo")
            if accept_promo:
                self.click("div.promo button.yes")
                self.assert_exact_text("cart (4)", 'a[aria-label="Cart page"]')
                promo = True
                total_string = "Total: $37.00"
            else:
                self.click("div.promo button.no")
        checkout_button = 'button[data-test="checkout"]'
        if promo and not self.browser == "safari":
            self.hover(checkout_button)
            if not self.is_element_visible("ul.cart-preview"):
                self.highlight(checkout_button)
                self.post_message("STOP moving the mouse!<br />Hover blocked!")
                self.hover(checkout_button)
            self.assert_text("(Discounted) Mocha", "ul.cart-preview")
        self.assert_exact_text(total_string, checkout_button)
        self.click(checkout_button)
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证右键菜单能正确添加咖啡到购物车')
    def test_context_click_add_coffee(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.context_click('div[data-test="Espresso_Macchiato"]')
        self.click('form button:contains("Yes")')
        self.assert_exact_text("cart (1)", 'a[aria-label="Cart page"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $12.00", 'button[data-test="checkout"]')
        self.click('button[data-test="checkout"]')
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('验证从购物车移除商品的功能')
    def test_remove_added_coffee(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", "button.pay")
        self.wait_for_element('div[class="cup-body"]')
        self.click_visible_elements('div[class="cup-body"]', limit=6)
        self.assert_exact_text("cart (6)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $74.00", 'button[data-test="checkout"]')
        self.click('a[aria-label="Cart page"]')
        self.click_visible_elements("button.delete")
        self.assert_text("No coffee, go add some.", "div#app")
        self.click('a[aria-label="Menu page"]')
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", 'button[data-test="checkout"]')