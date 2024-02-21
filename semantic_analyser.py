from selenium.webdriver.common.by import By
import main

actions = ["click", "verify", "check", "open", "close"]
verifications = ["displayed", "not displayed"]


def action_inputs(step, widget_components):
    by = get_by(step, widget_components)
    action_literal = extract_action(step)
    verification_literal = extract_verification(step)
    return by, action_literal, verification_literal


def get_by(step, widget_components):
    element = extract_element(step, widget_components)
    return match_element(element)


def match_action(action, by, verification=""):
    web_element = main.driver.find_element(by=by[0], value=by[1])
    match action:
        case "click":
            web_element.click()
        case "verify":
            match_verification(web_element, verification)


def match_element(element):
    match element:
        case "tooltip":
            return (
                By.CSS_SELECTOR,
                "div.by-line-tooltip"
            )
        case "medically reviewed":
            return (
                By.CSS_SELECTOR,
                ".by-line__verified-wrapper--medically-reviewed"
            )


def match_verification(web_element, verification):
    match verification:
        case "displayed":
            assert web_element.is_displayed()


def extract_action(step):
    for action in actions:
        if action in str(step).lower():
            return action


def extract_element(step, components):
    for element in components:
        if element in str(step).lower():
            return element


def extract_verification(step):
    for verification in verifications:
        if verification in str(step).lower():
            return verification
