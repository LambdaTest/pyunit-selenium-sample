import time
import os
from threading import Thread
from selenium import webdriver
import json


username = os.environ.get("LT_USERNAME")
access_key = os.environ.get("LT_ACCESS_KEY")

config = open('./config.json','r')
capabilites = json.load(config)


def get_browser(caps):
	return webdriver.Remote(
            command_executor="https://{}:{}@hub.lambdatest.com/wd/hub".format(username, access_key),
            desired_capabilities=caps
        )

# You can configure your test capabilities here 
browsers = [capabilites["parallel_test_1"], capabilites["parallel_test_2"]]

browsers_waiting = []

# Running the test cases
def get_browser_and_wait(browser_data):
	print ("starting %s" % browser_data["name"])
	browser = get_browser(browser_data)
	browser.get("https://lambdatest.com")
	browsers_waiting.append({"data": browser_data, "driver": browser})
	print ("%s ready" % browser_data["name"])
	while len(browsers_waiting) < len(browsers):
		print ("browser %s sending heartbeat while waiting" % browser_data["name"])
		browser.get("https://lambdatest.com")
		time.sleep(3)


thread_list = []
for i, browser in enumerate(browsers):
	t = Thread(target=get_browser_and_wait, args=[browser])
	thread_list.append(t)
	t.start()

for t in thread_list:
	t.join()


for i, b in enumerate(browsers_waiting):
	print ("browser %s's title: %s" % (b["data"]["name"], b["driver"].title))
	b["driver"].quit()
