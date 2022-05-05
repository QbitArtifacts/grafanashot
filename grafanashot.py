#!/usr/bin/env python3
import json
import sys

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) < 4:
    print("Usage: %s <user> <pass> (<dashboard_url>)+ <timeout>?" % sys.argv[0])
    exit(-1)

username = sys.argv[1]
password = sys.argv[2]
urls = sys.argv[3:]
if urls[-1].isnumeric():
    timeout = urls[-1]
    urls = urls[:-1]
else:
    timeout = 120

options = Options()
options.headless = True
service = Service('./bin/geckodriver')
driver = webdriver.Firefox(options=options, service=service)

# Wait for initialize, in seconds
wait = WebDriverWait(driver, timeout + 10)

driver.get(urls[0])

username_input = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input')

username_input.click()
username_input.send_keys(username)

password_input = driver.find_element(By.XPATH, '//*[@id="current-password"]')
password_input.click()
password_input.send_keys(password)

login_button = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]/div/div[2]/div/div/form/button')
login_button.click()

snapshots = {}
for url in urls:
    if url not in snapshots:
        driver.get(url)

        share_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div[3]/header/div/div[3]/div/button')))
        share_button.click()

        snapshot_tab = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/ul/li[2]/a')
        snapshot_tab.click()

        timeout_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="timeout-input"]')))
        timeout_str = str(timeout)
        timeout_input.send_keys(timeout_str)  # set wait timeout
        # delete before 4 seconds
        for i in range(len(timeout_str)):
            timeout_input.send_keys(Keys.ARROW_LEFT)
        timeout_input.send_keys(Keys.BACK_SPACE)

        expire_selector = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expire-select-input"]')))
        expire_selector.click()
        # set snapshot expire after 24h
        expire_selector.send_keys(Keys.ARROW_DOWN)
        expire_selector.send_keys(Keys.ARROW_DOWN)
        expire_selector.send_keys(Keys.ENTER)

        snapshot_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[5]/div/div[3]/button')))
        snapshot_button.click()

        snapshot_link = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[1]/div/a')))

        snapshots[url] = snapshot_link.get_attribute('href')

print(json.dumps(snapshots))

driver.close()
driver.quit()
