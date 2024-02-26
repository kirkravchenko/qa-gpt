from selenium.webdriver.common.by import By


class Byline:
    def __init__(self, widget_specific_description=""):
        self.widget_specific_description = widget_specific_description

    name = "byline"
    components = [
        ("tooltip", By.CSS_SELECTOR, "div.by-line-tooltip"),
        ("tooltip icon", By.CSS_SELECTOR, ".by-line-tooltip__top-left svg"),
        ("tooltip subheading", By.XPATH, "//span[@class='by-line-tooltip__subheading']"),
        ("tooltip body", By.CSS_SELECTOR, ".by-line-tooltip__body"),
        ("tooltip link", By.CSS_SELECTOR, ".by-line-tooltip__footer a"),
        ("tooltip close button", By.CSS_SELECTOR, ".by-line-tooltip__top-right svg"),
        ("medically reviewed button", By.XPATH, "//button[text()='Medically Reviewed']"),
        ("medically reviewed icon", By.CSS_SELECTOR, ".by-line__verified-wrapper--medically-reviewed svg"),
        ("author icon", By.XPATH, "//div[div[text()='By']]//img"),
        ("reviewer icon", By.XPATH, "//div[div[div[button[contains(text(),'Medically Reviewed')]]]]//img"),
        ("default author icon", By.XPATH, "//div[div[text()='By']]//*[local-name() = 'svg']"),
        ("default reviewer icon", By.XPATH, "//div[div[div[button[contains(text(),'Medically Reviewed')]]]]/div[@class='by-line__profile-icons']//*[local-name() = 'svg']"),
        ("author name", By.XPATH, "//div[text()='By']//a"),
        ("reviewer name", By.XPATH, "//div[div[button[contains(text(),'Medically Reviewed')]]]//a[@rel='author']"),
        ("last updated date", By.CSS_SELECTOR, ".by-line__last-updated-date"),
    ]
    components_names = list(map(lambda x: x[0], components))
    base_description = f"""Byline is a widget that is able to contain the 
    following components: {components_names}. Author name can be a link to the 
    author's page; reviewer name can be a link to reviewer's page. 
    'medically reviewed button' is a button that if you click on it, shows small 
    tooltip. The button has label 'MEDICALLY REVIEWED'. That tooltip contains 
    its own components listed above. Name components just as I listed before."""
