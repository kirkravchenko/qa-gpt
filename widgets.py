class Byline:
    name = "byline"
    components = [
        "author icon", "author name", "reviewer icon",
        "reviewer name", "medically reviewed", "tooltip", "author", "reviewer"
    ]
    description = f"""Byline is a widget that contains the following elements: 
    {components}. Author name can be a link to the author's page; reviewer name 
    can be a link to reviewer's page. 'medically reviewed' is a button that if 
    you click on it, shows small popup."""
