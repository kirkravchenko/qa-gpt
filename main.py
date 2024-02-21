from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import gpt
import widgets
import semantic_analyser

url = "https://www.everydayhealth.com/testpage/automationstatic/bylinearticle/"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)


def test_byline():
    get(url)
    byline = widgets.Byline()
    scenario = get_scenario_from("byline.feature")
    # scenario = gpt.generate_scenario_for(byline)
    perform(scenario, byline)
    time.sleep(1)
    driver.quit()


def perform(scenario, widget):
    for step in scenario:
        perform_next(step, widget)


def perform_next(step, widget):
    inputs = semantic_analyser.action_inputs(step, widget.components)
    perform_action(inputs)


def perform_action(inputs):
    by = inputs[0][0]
    selector = inputs[0][1]
    action = inputs[1]
    verification = inputs[2]
    web_element = driver.find_element(by=by, value=selector)
    match action:
        case "click":
            web_element.click()
        case "verify":
            perform_assert(verification, web_element)


def perform_assert(verification, web_element):
    match verification:
        case "displayed":
            assert web_element.is_displayed()


def get_scenario_from(path):
    with open(path) as steps:
        return steps.readlines()


def close_pop_ups():
    popup = driver.find_element(by=By.ID,
                                value="onetrust-accept-btn-handler")
    wait = WebDriverWait(driver, timeout=5)
    wait.until(lambda d: popup.is_displayed())
    popup.click()
    driver.find_element(by=By.CSS_SELECTOR,
                        value="button.fc-cta-consent").click()


def get(url):
    driver.get(url)
    close_pop_ups()
