import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

username = os.environ.get("LT_USERNAME")
access_key = os.environ.get("LT_ACCESS_KEY")


class FirstSampleTest(unittest.TestCase):
    def setUp(self):
        lt_options = {
            "build": "PyunitTest sample build",  # Change your build name here
            "name": "Py-unittest",              # Change your test name here
            "platformName": "Windows 10",       # Change your OS version here
            "browserName": "chrome",            # Change your browser here
            "browserVersion": "latest",         # Change your browser version here
        }

        options = Options()
        options.set_capability("LT:Options", lt_options)

        self.driver = webdriver.Remote(
            command_executor=f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub",
            options=options
        )

    def tearDown(self):
        self.driver.quit()

    def test_unit_user_should_able_to_add_item(self):
        driver = self.driver
        driver.get("https://www.testmuai.com/selenium-playground/todo-app/")

        driver.find_element("name", "li1").click()
        driver.find_element("name", "li2").click()
        driver.find_element("id", "sampletodotext").send_keys("Yey, Let's add it to list")
        driver.find_element("id", "addbutton").click()

        added_item = driver.find_element("xpath", "//input[@name='li6']/following-sibling::span").text
        print("Added item:", added_item)
        self.assertIn("Yey", added_item)


if __name__ == "__main__":
    unittest.main()
