import unittest
import time

from selenium import webdriver

class Module0Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login()

    def login(self):
        # Go to the first module
        self.driver.get("http://localhost:8000/accounts/login/")
        # Get the form fields to log in
        username = self.driver.find_element_by_id('id_login')
        password = self.driver.find_element_by_id('id_password')
        # Simulate entering the username and password
        username.send_keys("shuba.gooba.designs@gmail.com")
        password.send_keys("123abcde")
        # Submit the form
        form = self.driver.find_element_by_css_selector("button[type=submit]")
        form.click()

    def test_intro(self):
        self.driver.get("http://localhost:8000/0/intro")

        next_button = self.driver.find_element_by_id('next')
        next_button.click()

    def test_map(self):
        self.driver.get("http://localhost:8000/0/map")

        previous_link = self.driver.find_element_by_id('back')
        previous_link.click()

    def tearDown(self):
        self.driver.quit()