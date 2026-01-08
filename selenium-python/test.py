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
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# The chrome and chromedriver installation can take some time.
# Give 5 minutes to install everything.
TIMEOUT = 5 * 60 * 1000

def log_request(request):
    print(f"Request to: {request.url}")
    print("Headers:", request.headers)
    request.continue_request()

@pytest.fixture(scope="module")
def driver():
    # By default, the test uses the latest stable Chrome version.
    # Replace the "stable" with the specific browser version if needed,
    # e.g. 'canary', '115' or '144.0.7534.0' for example.
    browser_version = "stable"

    stableOption = Options()
    stableOption.add_argument("--headless")
    stableOption.add_argument("--no-sandbox")
    stableOption.enable_bidi = True
    stableOption.browser_version = browser_version
    # Enable WebDriver BiDi
    stableOption.set_capability("webSocketUrl", True)

    service = Service(service_args=["--log-path=chromedriver.log", "--verbose"])

    driver = webdriver.Chrome(options=stableOption, service=service)

    yield driver

    driver.quit()

@pytest.mark.timeout(TIMEOUT)
def test_should_be_able_to_navigate_to_google_com(driver):
    """This test is intended to verify the setup is correct."""
    driver.get("https://www.google.com")
    logging.info(driver.title)
    assert driver.title == "Google"

@pytest.mark.timeout(TIMEOUT)
def test_from_issue(driver):
    options = webdriver.ChromeOptions()
    options.set_capability("webSocketUrl", True)
    options.enable_bidi = True
    options.browser_version = "121"
    customDriver = webdriver.Chrome(options=options)

    customDriver.network.add_request_handler(
        event="before_request",
        callback=log_request,
    )

    customDriver.get("https://www.google.com")

    time.sleep(5)
    assert customDriver.title == "Google"
    customDriver.quit()
