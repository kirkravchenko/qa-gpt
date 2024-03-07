from openai import OpenAI
from jproperties import Properties
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
    The list of possible action strings: {semantic_analyser.get_actions()}
    The list of possible verification strings: 
    {semantic_analyser.get_possible_verifications()}
    Here is a schema of scenario:
    {{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {{
    "scenario": {{
      "type": "array",
      "items": [
        {{
          "type": "object",
          "properties": {{
            "action": {{
              "type": "string"
            }},
            "component": {{
              "type": "string"
            }},
            "verification": {{
              "type": "string"
            }},
            "value": {{
              "type": "string"
            }}
          }},
          "required": [
            "action",
            "component",
            "verification",
            "value"
          ]
        }}
      ]
    }}
  }},
  "required": [
    "scenario"
  ]
}}
    The generated scenario should be in a JSON format. Each step of the 
    scenario is a JSON object:
    {{ 
        "action": "<action string>", 
        "component": "<component name>", 
        "verification": "<verification string>",
        "value": "<text value of component, if any>"
    }}
    Each field in JSON is required!
    Generate minimum 12 steps per scenario, maximum 30 steps.
    Generate scenario inside triple quotes.
    Keep test steps as simple, short as 
    possible. Per one step verify only one component. Use terms from widget 
    description.
    No need to mention opening the webpage as a first step. 
    'page is opened' is not a component. If you generate a step where page
    is opened, make sure to append a step to navigate back. 
    If you generate a step where user click on link which opens a page, 
    make sure to append a step to navigate back.
    Each step contains ONLY ONE verification! This step is an error, since 
    it contains 2 verifications: in 'component' and in 'verification'.
    {{'action': 'verify', 'component': 'page is opened', 'verification': 'page title contains', 'value': ''}}
    Just respond with JSON, don't write any comments"""


example_from_user_prompt = """
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
      "component": "",
      "verification": "page is opened",
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
