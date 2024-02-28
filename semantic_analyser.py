import re
from enum import Enum

import widgets


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
    TEXT_PRESENT = "text is present"


actions = [
    Action.CLICK.value,
    Action.DOUBLE_CLICK.value,
    Action.VERIFY.value
]

# regex
text_in_brackets_regex = "'(.+)'|\"(.+)\""

# conjunctions
and_conjunction = " and "
# TODO for the following step 'Click on 'medically reviewed button' tooltip
#  and verify 'tooltip icon' is displayed.' think of conjunction splitting


class VerificationPattern:
    def __init__(self, regex, text):
        self.text = text
        self.regex = regex


verification_patterns = [
    VerificationPattern(
        "('(.+)'|\"(.+)\") text is present",
        VerificationItem.TEXT_PRESENT.value,
    ),
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
    verifications_list = extract_verifications(step)
    verifications_list = process_verifications(verifications_list)
    step_inputs = StepInputs(by, action_literal, verifications_list, step)
    return step_inputs


def get_by(step, components):
    element_literal = extract_element(step, components)
    return match_element_get_by(element_literal, components)


def match_element_get_by(element_literal, components):
    for component in components:
        if element_literal is component.name:
            return component.by, component.selector


def extract_action(step):
    for action in actions:
        if action in str(step).lower():
            return action
    return ""


def extract_element(step, components=None):
    if components is None:
        components = [widgets.WidgetComponent("", "")]
    for component in components:
        conjunctions = component.get_actions_components_conjunctions()
        if conjunctions:
            for conjunction in conjunctions:
                if conjunction in str(step).lower():
                    return component.name


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


def process_verifications(verifications_list):
    verifications_list = process_present_verifications(verifications_list)
    return verifications_list


def process_present_verifications(verifications_list):
    def verification_actions(verification=Verification("", "")):
        return verification.verification_action

    verification_actions_list = list(
        map(verification_actions, verifications_list))
    if VerificationItem.TEXT_PRESENT.value in verification_actions_list:
        if VerificationItem.IS_PRESENT.value in verification_actions_list:
            for verification in verifications_list:
                if (verification.verification_action ==
                        VerificationItem.IS_PRESENT.value):
                    verifications_list.remove(verification)
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
