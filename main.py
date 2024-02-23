from selenium import webdriver
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import gpt
import widgets
import semantic_analyser
from jproperties import Properties

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)


def test_byline():
    get(get_test_url())
    byline = widgets.Byline(
        """author icon is displayed, default reviewer icon is displayed;
        author name is 'testauthor_active1', reviewer name is 
        'Mr Test Automation, MPH', last updated date has 
        text 'November 30, 2018'"""
    )
    scenario = get_scenario_from("byline.feature")
    # scenario = gpt.generate_scenario_for(byline)
    perform(scenario, byline)
    time.sleep(1)
    driver.quit()


def perform(scenario, widget):
    for step in scenario:
        perform_next(step, widget)


def perform_next(step, widget):
    step_inputs = semantic_analyser.get_step_inputs(step, widget.components)
    perform_action(step_inputs)


def perform_action(step_inputs):
    by = step_inputs.by[0]
    selector = step_inputs.by[1]
    action = step_inputs.action_literal
    verifications = step_inputs.verifications_objs
    web_element = driver.find_element(by=by, value=selector)
    match action:
        case "click":
            web_element.click()
        case "double click":
            ActionChains(driver).double_click(web_element).perform()
        case "verify":
            for verification in verifications:
                perform_assert(verification, web_element)


def perform_assert(verification, web_element):
    match verification.verification_action:
        case "is displayed":
            assert web_element.is_displayed()
        case "is present":
            assert web_element.is_displayed()
        case "is not displayed":
            assert not web_element.is_displayed()
        case "is not present":
            assert not web_element.is_displayed()
        case "is a link":
            assert web_element.get_attribute("href") is not None
        case "text is":
            actual = web_element.text
            expected = verification.expected_value
            assert actual == expected


def get_scenario_from(path):
    with open(path) as steps:
        return steps.readlines()


def close_pop_ups():
    popup = driver.find_element(
        by=By.ID,
        value="onetrust-accept-btn-handler"
    )
    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d: popup.is_displayed())
    popup.click()
    driver.find_element(
        by=By.CSS_SELECTOR,
        value="button.fc-cta-consent"
    ).click()


def get(url):
    driver.get(url)
    close_pop_ups()


def get_test_url():
    configs = Properties()
    with open('other.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get("url")[0]
