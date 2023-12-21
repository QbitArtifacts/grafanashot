#!/usr/bin/env python3
import json
import logging
import sys
import traceback

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support import expected_conditions as EC


class GrafanaShot:
    def __init__(self, headless=True):
        options = Options()
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        if headless:
            options.add_argument('--headless')
        service = Service('./bin/geckodriver')
        self.driver = webdriver.Firefox(options=options, service=service)
        self.clear()

    def open_url(self, url):
        self.driver.get(url)

    def clear(self):
        self.open_url('about:blank')

    def login(self, url, user, passw):
        self.driver.get(url)

        username_input = self.driver.find_element(By.XPATH,
            '/html/body/div/div[1]/div/main/div/div/div[3]/div/div/div[2]/div/div/form/div[1]/div[2]/div/div/div/input'
        )

        username_input.click()
        username_input.send_keys(user)

        password_input = self.driver.find_element(By.XPATH, '//*[@id="current-password"]')
        password_input.click()
        password_input.send_keys(passw)

        login_button = self.driver.find_element(By.XPATH,
                                                '/html/body/div/div[1]/div/main/div/div/div[3]/div/div/div[2]/div/div/form/button')
        login_button.click()

    def logout(self):
        pass

    def get_url(self):
        return self.driver.current_url

    def get_snapshot(self, url, timeout):
        # Wait for initialize, in seconds
        wait = WebDriverWait(self.driver, timeout + 10)

        self.driver.get(url)

        share_button = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/button')))
        share_button.click()

        snapshot_tab = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/a')
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

        snapshot_button = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[5]/div/div[3]/button')))
        snapshot_button.click()

        snapshot_link = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="snapshot-url-input"]')))

        return snapshot_link.get_attribute('value')

    def close_driver(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Usage: %s <user> <pass> (<dashboard_url>)+ <timeout>?" % sys.argv[0])
        exit(-1)

    username = sys.argv[1]
    password = sys.argv[2]
    urls = sys.argv[3:]
    if urls[-1].isnumeric():
        timeout = int(urls[-1])
        urls = urls[:-1]
    else:
        timeout = 120

    grafana = GrafanaShot()

    try:
        grafana.login(urls[0], username, password)

        snapshots = {}
        for url in urls:
            if url not in snapshots:
                result = grafana.get_snapshot(url, timeout)
                snapshots[url] = result

        grafana.close_driver()
        print(json.dumps(snapshots))
    except Exception as e:
        grafana.close_driver()
        print("<<<<<<< SNAPSHOT FAILED >>>>>>>>")
        logging.error(traceback.format_exc())
        exit(1)
