from selenium.webdriver.common.by import By


class WidgetComponent:
    def __init__(self, name, selector, by=By.ID, possible_actions=None):
        if possible_actions is None:
            possible_actions = []
        self.name = name
        self.selector = selector
        self.by = by
        self.possible_actions = possible_actions

    def get_actions_components_conjunctions(self):
        actions_components_conjunctions = []
        for possible_action in self.possible_actions:
            actions_components_conjunctions.append(
                possible_action + " '" + self.name + "'"
            )
        return actions_components_conjunctions


class Byline:
    def __init__(self, widget_specific_description=""):
        self.widget_specific_description = widget_specific_description

    name = "byline"
    components = [
        WidgetComponent(
            "tooltip", "div.by-line-tooltip", By.CSS_SELECTOR,
            ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "tooltip icon", ".by-line-tooltip__top-left svg",
            By.CSS_SELECTOR, ["verify"]
        ),
        WidgetComponent(
            "tooltip subheading",
            "//span[@class='by-line-tooltip__subheading']", By.XPATH,
            ["verify"]
        ),
        WidgetComponent(
            "tooltip body", ".by-line-tooltip__body",
            By.CSS_SELECTOR, ["verify"]
        ),
        WidgetComponent(
            "tooltip link", ".by-line-tooltip__footer a",
            By.CSS_SELECTOR, ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "tooltip close button",
            ".by-line-tooltip__top-right svg",
            By.CSS_SELECTOR, ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "medically reviewed button",
            "//button[text()='Medically Reviewed']", By.XPATH,
            ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "medically reviewed icon",
            ".by-line__verified-wrapper--medically-reviewed svg",
            By.CSS_SELECTOR, ["verify"]
        ),
        WidgetComponent(
            "author icon", "//div[div[text()='By']]//img",
            By.XPATH, ["verify"]
        ),
        WidgetComponent(
            "reviewer icon",
            "//div[div[div[button[contains(text(),'Medically Reviewed')"
            "]]]]//img", By.XPATH, ["verify"]
        ),
        WidgetComponent(
            "default author icon",
            "//div[div[text()='By']]//*[local-name() = 'svg']",
            By.XPATH, ["verify"]
        ),
        WidgetComponent(
            "default reviewer icon",
            "//div[div[div[button[contains(text(),"
            "'Medically Reviewed')]]]]/div[@class='by-line__profile-icons']"
            "//*[local-name() = 'svg']", By.XPATH, ["verify"]
        ),
        WidgetComponent(
            "author name", "//div[text()='By']//a",
            By.XPATH, ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "reviewer name",
            "//div[div[button[contains(text(),'Medically Reviewed')]]]"
            "//a[@rel='author']",
            By.XPATH, ["click", "click on", "verify"]
        ),
        WidgetComponent(
            "last updated date", ".by-line__last-updated-date",
            By.CSS_SELECTOR, ["verify"]
        ),
    ]
    components_names = list(map(lambda x: x.name, components))
    base_description = f"""Byline is a widget that is able to contain the 
    following components. The list of possible component strings: 
    {components_names}.\nAuthor name can be a link to the 
    author's page; reviewer name can be a link to reviewer's page. 
    'medically reviewed button' is a button that if you click on it, shows small 
    tooltip. The button has label 'MEDICALLY REVIEWED'. That tooltip contains 
    its own components listed above. Name components just as I listed before"""
