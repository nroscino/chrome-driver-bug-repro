// Copyright 2025 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.IO;
using System.Text.RegularExpressions;

namespace RegressionTest;

public class Tests
{
  [Test]
  public void ShouldBeAbleToNavigateAfterDeletingNetworkConditions()
  {
    var options = new ChromeOptions();
    options.AddArgument("--headless");
    options.AddArgument("--no-sandbox");
    // By default, the test uses the latest stable Chrome version.
    // Replace the "stable" with the specific browser version if needed,
    // e.g. 'canary', '115' or '144.0.7534.0' for example.
    options.BrowserVersion = "stable";

    var service = ChromeDriverService.CreateDefaultService();
    service.LogPath = "d:\\chromedriver.log";
    service.EnableVerboseLogging = true;

    IWebDriver driver = new ChromeDriver(service, options);

    try
    {
      driver.Navigate().GoToUrl("https://www.google.com");
      Assert.That(driver.Title, Is.EqualTo("Google"));
    }
    finally
    {
      driver.Quit();
    }
  }

  // Reproducing crbug/42323674
  [Test]
  public void IssueReproduction()
  {
    string baseURL = "https://pegelonline.wsv.de/webservice/dokuRestapi";

    var options = new ChromeOptions();
    var options2 = new ChromeOptions();
    options2.BrowserVersion = "119";

    options.AddArgument("--headless");
    options.AddArgument("--no-sandbox");
    options.BrowserVersion = "119";

    var service = ChromeDriverService.CreateDefaultService();
    service.LogPath = "d:\\chromedriver.log";
    service.EnableVerboseLogging = true;

    IWebDriver driver = new ChromeDriver(service, options);
    IWebDriver driver2 = new ChromeDriver(service, options);

    try
    {
      string res1 = printLinks(driver, baseURL);
      string res2 = printLinks(driver2, baseURL);

      Assert.That(res1,Is.EqualTo(res2));
    }
    finally
    {
      driver.Quit();
    }
  }

  private string printLinks(IWebDriver driver, string baseURL) {
    driver.Navigate().GoToUrl(baseURL);
    var link = driver.FindElement(By.XPath("/html/body/div/div[8]/table[5]/tbody/tr[2]/td[1]/a"));
    return link.GetAttribute("href");
  }
}
