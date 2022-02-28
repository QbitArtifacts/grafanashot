#!/usr/bin/env python3
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) != 4:
    print("Usage: %s <dashboard_url> [<user> <pass>]" % sys.argv[0])
    exit(-1)

full_url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

options = Options()
options.headless = True
service = Service('./bin/geckodriver')
driver = webdriver.Firefox(options=options, service=service)
driver.get(full_url)

# Wait for initialize, in seconds
wait = WebDriverWait(driver, 30)

username_input = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input')

username_input.click()
username_input.send_keys(username)

password_input = driver.find_element(By.XPATH, '//*[@id="current-password"]')
password_input.click()
password_input.send_keys(password)

login_button = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]/div/div[2]/div/div/form/button')
login_button.click()


share_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/main/div[3]/header/div/div[3]/div/button')))
share_button.click()

snapshot_tab = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/ul/li[2]/a')
snapshot_tab.click()

snapshot_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[5]/div/div[3]/button')))
snapshot_button.click()

snapshot_link = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[1]/div/a')))

print(snapshot_link.get_attribute('href') + '?kiosk')

driver.close()
driver.quit()
