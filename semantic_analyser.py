import re
from selenium.webdriver.common.by import By
from enum import Enum


class Action(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double click"
    VERIFY = "verify"


class VerificationItem(Enum):
    IS_DISPLAYED = "is displayed"
    IS_PRESENT = "is present"
    NOT_DISPLAYED = "not displayed"
    NOT_PRESENT = "not present"
    IS_LINK = "is a link"
    TEXT_IS = "text is"
    TEXT_CONTAINS = "text contains"
    PAGE_IS_OPENED = "page is opened"


actions = [
    Action.CLICK.value,
    Action.DOUBLE_CLICK.value,
    Action.VERIFY.value
]

# regex
text_in_brackets_regex = "'(.+)'|\"(.+)\""


# a list of tuples. each tuple contains:
# [0] - verification with possible regex
# [1] - verification without regex
# if regex version doesn't actually contain regex -
# it will be same as verification in [1]

class VerificationPattern:
    def __init__(self, regex, text):
        self.text = text
        self.regex = regex


verification_patterns = [
    VerificationPattern(
        VerificationItem.IS_PRESENT.value,
        VerificationItem.IS_PRESENT.value
    ),
    VerificationPattern(
        VerificationItem.IS_DISPLAYED.value,
        VerificationItem.IS_DISPLAYED.value
    ),
    VerificationPattern(
        VerificationItem.NOT_DISPLAYED.value,
        VerificationItem.NOT_DISPLAYED.value
    ),
    VerificationPattern(
        VerificationItem.NOT_PRESENT.value,
        VerificationItem.NOT_PRESENT.value
    ),
    VerificationPattern(
        "text is '(.+)'|text is \"(.+)\"",
        VerificationItem.TEXT_IS.value
    ),
    VerificationPattern(
        "text contains '(.+)'|text contains \"(.+)\"",
        VerificationItem.TEXT_CONTAINS.value
    ),
    VerificationPattern(
        VerificationItem.IS_LINK.value, VerificationItem.IS_LINK.value
    ),
    VerificationPattern(
        VerificationItem.PAGE_IS_OPENED.value,
        VerificationItem.PAGE_IS_OPENED.value
    )
]


def get_step_inputs(step, components):
    by = get_by(step, components)
    action_literal = extract_action(step)
    verifications_objs = extract_verifications(step)
    step_inputs = StepInputs(by, action_literal, verifications_objs, step)
    return step_inputs


def get_by(step, components):
    element_literal = extract_element(step, components)
    return match_element_get_by(element_literal, components)


def match_element_get_by(element_literal, components):
    for component in components:
        expected_literal, by, selector = component
        if element_literal is expected_literal:
            return by, selector
    return By.ID, ""


def extract_action(step):
    for action in actions:
        if action in str(step).lower():
            return action
    return ""


def extract_element(step, components):
    for component in components:
        element_literal = component[0]
        if "'" + element_literal + "'" in str(step).lower():
            return element_literal


def extract_verifications(step):
    verifications_list = []
    for verification_pattern in verification_patterns:
        verification_action = verification_pattern.text
        verification_obj = Verification(verification_action, "")
        verification_match = re.search(verification_pattern.regex, str(step))
        if verification_match:
            expected_text_match = re.search(
                text_in_brackets_regex, verification_match.group(0)
            )
            if expected_text_match:
                expected_text = expected_text_match.group(0)
                verification_obj.expected_value = (
                    expected_text.replace("'", "")
                )
            verifications_list.append(verification_obj)
    return verifications_list


class StepInputs:
    def __init__(self, by, action_literal, verifications_objs, step):
        self.by = by
        self.action_literal = action_literal
        self.verifications_objs = verifications_objs
        self.step = step


class Verification:
    def __init__(self, verification_action, expected_value):
        self.verification_action = verification_action
        self.expected_value = expected_value
