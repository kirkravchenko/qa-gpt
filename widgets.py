from selenium.webdriver.common.by import By


class Byline:
    name = "byline"
    components = [
        ("tooltip", By.CSS_SELECTOR, "div.by-line-tooltip"),
        ("medically reviewed", By.CSS_SELECTOR, ".by-line__verified-wrapper--medically-reviewed"),
        ("author icon", By.CSS_SELECTOR, ""),
        ("author name", By.CSS_SELECTOR, ""),
        ("reviewer icon", By.CSS_SELECTOR, ""),
        ("reviewer name", By.CSS_SELECTOR, ""),
        ("author", By.CSS_SELECTOR, ""),
        ("reviewer", By.CSS_SELECTOR, "")
    ]
    components_names = list(map(lambda x: x[0], components))
    description = f"""Byline is a widget that contains the following elements: 
    {components_names}. Author name can be a link to the author's page; reviewer name 
    can be a link to reviewer's page. 'medically reviewed' is a button that if 
    you click on it, shows small popup."""