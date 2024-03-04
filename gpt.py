from openai import OpenAI
from jproperties import Properties
import json
import semantic_analyser

def get_openai_property(prop):
    configs = Properties()
    with open('openai.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop)[0]


def request_gpt(prompt_text):
    client = OpenAI(api_key=get_openai_property("openAI_token"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt_text,
            }
        ],
        model=get_openai_property("model"),
    )
    response = chat_completion.choices[0].message.content
    # response = list(filter(None, response.splitlines()[1:]))
    return response


def prompt(widget):
    return f"""I wrote Python method that takes as input description of actions 
    and performs the actions using Selenium WebDriver. Current web page contains 
    {widget.name} widget. Widget description: {widget.base_description} 
    Properties of this particular widget: {widget.widget_specific_description} 
    I want you to generate one test scenario for this specific widget that I 
    can use as input for my Python method.
    The list of possible action strings: {semantic_analyser.get_actions()}\n
    The list of possible verification strings: {semantic_analyser.get_possible_verifications()}\n
    The generated scenario should be in a JSON format. Each step of the 
    scenario is a JSON object:\n
    {{ 
        "action": "<action string>", 
        "component": "<component name>", 
        "verification": "<verification string>",
        "value": "<text value of component, if any>"
    }}\n 
    Each filed in JSON is required!
    Keep test steps as simple, short as 
    possible. Per one step verify only one component. Use terms from widget 
    description. As user actions use these verbs: click, verify.\n 
    The list of verification verbs: displayed, not displayed, present, not 
    present, page is opened, <component name> text is, <component name> text 
    contains. Use verbs that are concrete, not ambiguous or abstract. 
    No need to mention opening the webpage as a first step. 
    'page is opened' is not a component. If you generate a step where page
    is opened, make sure to append a step to navigate back. 
    If you generate a step where user click on link, make sure to append a 
    step to navigate back.\n
    Just respond with JSON, don't write any comments"""


example_from_user_prompt="""
Here is an example of generated scenario.
{
  "scenario": [
    {
      "action": "verify",
      "component": "author icon",
      "verification": "is displayed",
      "value": ""
    },
    {
      "action": "verify",
      "component": "default reviewer icon",
      "verification": "is displayed",
      "value": ""
    },
    {
      "action": "verify",
      "component": "author name",
      "verification": "text is",
      "value": "testauthor_active1"
    },
    {
      "action": "verify",
      "component": "reviewer name",
      "verification": "text is",
      "value": "Mr Test Automation, MPH"
    },
    {
      "action": "verify",
      "component": "last updated date",
      "verification": "text is",
      "value": "on November 30, 2018"
    },
    {
      "action": "verify",
      "component": "medically reviewed button",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "click",
      "component": "medically reviewed button",
      "verification": "",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip icon",
      "verification": "is displayed",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip subheading",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip body",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip link",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip close button",
      "verification": "is present",
      "value": ""
    },
    {
      "action": "click",
      "component": "tooltip link",
      "verification": "",
      "value": ""
    },
    {
      "action": "verify",
      "component": "page is opened",
      "verification": "is true",
      "value": ""
    },
    {
      "action": "navigate back",
      "component": "",
      "verification": "",
      "value": ""
    },
    {
      "action": "click",
      "component": "tooltip close button",
      "verification": "",
      "value": ""
    },
    {
      "action": "verify",
      "component": "tooltip",
      "verification": "not displayed",
      "value": ""
    }
  ]
}
"""


def generate_scenario_for(widget):
    return request_gpt(prompt(widget))


def print_prompt(widget):
    print(f'prompt: {prompt(widget)}')


def print_response(response):
    print("\nGenerated scenario")
    for line in response:
        print(line)
