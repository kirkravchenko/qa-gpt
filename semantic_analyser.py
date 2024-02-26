import re

actions = ["click", "double click", "verify", "check", "open", "close"]

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
    VerificationPattern("is present", "is present"),
    VerificationPattern("is displayed", "is displayed"),
    VerificationPattern("not displayed", "not displayed"),
    VerificationPattern("not present", "not present"),
    VerificationPattern("text is '(.+)'|text is \"(.+)\"", "text is"),
    VerificationPattern("text contains '(.+)'|text contains \"(.+)\"", "text contains"),
    VerificationPattern("is a link", "is a link"),
]


def get_step_inputs(step, components):
    by = get_by(step, components)
    action_literal = extract_action(step)
    verifications_objs = extract_verifications(step)
    step_inputs = StepInputs(by, action_literal, verifications_objs)
    return step_inputs


def get_by(step, components):
    element_literal = extract_element(step, components)
    return match_element_get_by(element_literal, components)


def match_element_get_by(element_literal, components):
    for component in components:
        expected_literal, by, selector = component
        if element_literal is expected_literal:
            return by, selector


def extract_action(step):
    for action in actions:
        if action in str(step).lower():
            return action


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
    def __init__(self, by, action_literal, verifications_objs):
        self.by = by
        self.action_literal = action_literal
        self.verifications_objs = verifications_objs


class Verification:
    def __init__(self, verification_action, expected_value):
        self.verification_action = verification_action
        self.expected_value = expected_value
