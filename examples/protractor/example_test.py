from seleniumbase import BaseCase

import pytest
BaseCase.main(__name__, __file__)


class AngularJSHomePageTests(BaseCase):

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P0')
    @pytest.mark.description('Test AngularJS greeting functionality - user types name and sees personalized greeting')
    def test_greet_user(self):
        self.open("http://www.angularjs.org")
        self.type('[ng-model="yourName"]', "Julie")
        self.assert_exact_text("Hello Julie!", "h1.ng-binding")

    @pytest.mark.owner('caijinwei')
    @pytest.mark.priority('P1')
    @pytest.mark.description('Test AngularJS todo list functionality - verify existing todos and add new todo item')
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
