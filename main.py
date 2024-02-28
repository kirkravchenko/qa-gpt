import pytest
from selenium import webdriver
import time

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import gpt
import widgets
import semantic_analyser
from jproperties import Properties


class ClickedElement:
    def __init__(self, href="", text=""):
        self.href = href
        self.text = text


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
clicked_element = ClickedElement()


def test_byline():
    get(get_test_url())
    byline = widgets.Byline(
        """author icon is displayed, default reviewer icon is displayed;
        author name is 'testauthor_active1', reviewer name is 
        'Mr Test Automation, MPH', last updated date text is 
        'on November 30, 2018'"""
    )
    scenario = get_scenario_from("byline/5.feature")
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
    try:
        web_element = driver.find_element(by=by, value=selector)
    except NoSuchElementException:
        web_element = None
    match action:
        case semantic_analyser.Action.CLICK.value:
            global clicked_element
            clicked_element.href = web_element.get_attribute("href")
            clicked_element.text = web_element.text
            web_element.click()
        case semantic_analyser.Action.DOUBLE_CLICK.value:
            ActionChains(driver).double_click(web_element).perform()
        case semantic_analyser.Action.VERIFY.value:
            for verification in verifications:
                perform_assert(verification, web_element, step_inputs.step)
        case _:
            pytest.fail(f"no action matched in step '{step_inputs.step}'")


def perform_assert(verification, web_element, step):
    match verification.verification_action:
        case semantic_analyser.VerificationItem.IS_DISPLAYED.value:
            assert web_element.is_displayed()
        case semantic_analyser.VerificationItem.NOT_DISPLAYED.value:
            if web_element is None:
                return
            assert web_element.is_displayed() is False
        case semantic_analyser.VerificationItem.NOT_PRESENT.value:
            if web_element is None:
                return
            assert web_element.is_displayed() is False
        case semantic_analyser.VerificationItem.IS_LINK.value:
            assert web_element.get_attribute("href") is not None
        case semantic_analyser.VerificationItem.TEXT_IS.value:
            actual = web_element.text
            expected = verification.expected_value
            assert actual == expected
        case semantic_analyser.VerificationItem.TEXT_PRESENT.value:
            assert (get_web_element_by_text(verification.expected_value)
                    .is_displayed())
        case semantic_analyser.VerificationItem.IS_PRESENT.value:
            assert web_element.is_displayed()
        case semantic_analyser.VerificationItem.TEXT_CONTAINS.value:
            actual = web_element.text
            expected = verification.expected_value
            assert expected in actual
        case semantic_analyser.VerificationItem.PAGE_IS_OPENED.value:
            expected_url = get_relative_path(clicked_element.href)
            actual_url = get_relative_path(driver.current_url)
            assert actual_url == expected_url
        case _:
            pytest.fail(f"no verification matched in step '{step}'")


def get_web_element_by_text(expected_value):
    try:
        web_element = driver.find_element(
            By.XPATH, f"//*[text()='{expected_value}']"
        )
        return web_element
    except NoSuchElementException:
        expected_value = (str(expected_value).lower().title())
        web_element = driver.find_element(
            By.XPATH, f"//*[text()='{expected_value}']"
        )
        return web_element

def get_scenario_from(path):
    with open(path) as steps:
        return steps.readlines()


def close_pop_ups():
    wait = WebDriverWait(driver, timeout=5)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.ID, "onetrust-accept-btn-handler")
    ))
    popup = driver.find_element(
        by=By.ID,
        value="onetrust-accept-btn-handler"
    )
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
        return get_base_url() + configs.get("test_url")[0]


def get_base_url():
    configs = Properties()
    with open('other.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get("base_url")[0]


def get_eh_url_regex():
    configs = Properties()
    with open('other.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get("eh_url_regex")[0]


def get_relative_path(absolute_path=get_base_url()):
    try:
        return absolute_path.split(get_eh_url_regex())[1]
    except IndexError:
        return "/"
