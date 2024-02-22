actions = ["click", "verify", "check", "open", "close"]
verifications = ["displayed", "not displayed"]


def action_inputs(step, components):
    by = get_by(step, components)
    action_literal = extract_action(step)
    verification_literal = extract_verification(step)
    return by, action_literal, verification_literal


def get_by(step, components):
    element_literal = extract_element(step, components)
    return match_element_get_by(element_literal, components)


def match_element_get_by(element_literal, components):
    for component in components:
        expected_literal, by, selector = component
        if element_literal is expected_literal:
            return by, selector


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
        element_literal = element[0]
        if element_literal in str(step).lower():
            return element_literal


def extract_verification(step):
    for verification in verifications:
        if verification in str(step).lower():
            return verification
