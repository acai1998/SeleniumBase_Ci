from seleniumbase import BaseCase

import pytest
BaseCase.main(__name__, __file__)


class AngularJSHomePageTests(BaseCase):

    @pytest.mark.owner('liuyang')
    @pytest.mark.priority('P2')
    @pytest.mark.description('Test AngularJS greeting: user types name and page shows personalized Hello message')
    def test_greet_user(self):
        self.open("http://www.angularjs.org")
        self.type('[ng-model="yourName"]', "Julie")
        self.assert_exact_text("Hello Julie!", "h1.ng-binding")

    @pytest.mark.owner('wubin')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test AngularJS todo list: verify initial todos count and add a new todo item')
    def test_todo_list(self):
        self.open("http://www.angularjs.org")
        todo_selector = '[ng-repeat="todo in todoList.todos"]'
        # Verify that the todos are listed
        self.wait_for_element(todo_selector)
        todos = self.find_visible_elements(todo_selector)
        self.assert_equal(len(todos), 2)
        self.assert_equal(todos[1].text.strip(), "build an AngularJS app")
        # Verify adding a new todo
        self.type('[ng-model="todoList.todoText"]', "write a protractor test")
        self.click('[value="add"]')
        todos = self.find_visible_elements(todo_selector)
        self.assert_equal(len(todos), 3)
        self.assert_equal(todos[2].text.strip(), "write a protractor test")

    @pytest.mark.owner('chenmei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test AngularJS homepage title contains AngularJS and main navigation link is visible')
    def test_page_title_and_nav(self):
        self.open("http://www.angularjs.org")
        self.assert_title_contains("AngularJS")
        self.assert_element('a[href="http://www.angularjs.org"]')

    @pytest.mark.owner('wangwu')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test AngularJS todo item can be marked as done by clicking the checkbox')
    def test_todo_mark_done(self):
        self.open("http://www.angularjs.org")
        todo_selector = '[ng-repeat="todo in todoList.todos"]'
        self.wait_for_element(todo_selector)
        # Mark the first todo as done
        done_checkbox = 'input[ng-model="todo.done"]'
        self.assert_false(self.is_selected(done_checkbox))
        self.click(done_checkbox)
        self.assert_true(self.is_selected(done_checkbox))

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('测试用例说明')
    def test_basics(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_exact_text("Products", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("Your Cart", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click('button:contains("Remove")')  # HTML innerText
        self.assert_text_not_visible("Backpack", "div.cart_item")
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")