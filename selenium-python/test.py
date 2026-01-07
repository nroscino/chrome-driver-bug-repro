#  Copyright 2025 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# The chrome and chromedriver installation can take some time.
# Give 5 minutes to install everything.
TIMEOUT = 5 * 60 * 1000


@pytest.fixture(scope="module")
def driver():
    # By default, the test uses the latest stable Chrome version.
    # Replace the "stable" with the specific browser version if needed,
    # e.g. 'canary', '115' or '144.0.7534.0' for example.
    browser_version = "stable"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.browser_version = browser_version

    service = Service(service_args=["--log-path=chromedriver.log", "--verbose"])

    driver = webdriver.Chrome(options=options, service=service)

    yield driver

    driver.quit()


@pytest.mark.timeout(TIMEOUT)
def test_should_be_able_to_navigate_to_google_com(driver):
    """This test is intended to verify the setup is correct."""
    driver.get("https://www.google.com")
    logging.info(driver.title)
    assert driver.title == "Google"


@pytest.mark.timeout(TIMEOUT)
def test_issue_reproduction(driver):
    """Reproducing the local storage timeout issue.
    The bug report suggests that calling execute_script to set an item in localStorage
    causes a timeout in Chrome 107+.
    """
    driver.get("https://www.google.com")
    # Using the EXACT logic from the bug report.
    # driver.execute_script(f"window.localStorage.setItem('fp',{'123'});")
    # In Python, f"{'123'}" evaluates to "123".
    # So f"window.localStorage.setItem('fp',{'123'});" evaluates to 
    # "window.localStorage.setItem('fp',123);"
    driver.execute_script(f"window.localStorage.setItem('fp',{'123'});")
    
    # Verify the value is set correctly.
    val = driver.execute_script("return window.localStorage.getItem('fp');")
    assert val == "123"
