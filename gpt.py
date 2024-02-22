from openai import OpenAI
from jproperties import Properties

model = "gpt-3.5-turbo"


def get_openai_token():
    configs = Properties()
    with open('openai_token.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get("openAI_token")[0]


def request_gpt(prompt):
    client = OpenAI(api_key=get_openai_token())
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    response = chat_completion.choices[0].message.content
    print(f'response: {response}')
    return response


def prompt(widget):
    return f"""I wrote Python method that takes as input description of actions 
    and performs the actions using Selenium WebDriver. Current web page contains 
    {widget.name} widget. Widget description: {widget.base_description} 
    Properties of this particular widget: {widget.widget_specific_description} 
    I want you to generate one test scenario for this specific widget that I 
    can use as input for my Python method. Keep test steps as simple, short as 
    possible. Use terms from widget description. As user actions use set of 
    these verbs: click, open, close, verify, check. As verification verbs use 
    these set: displayed, not displayed, present, not present, other verbs that 
    are concrete, not ambiguous or abstract.
    No need to mention opening the webpage as a first step. """


def generate_scenario_for(widget):
    return request_gpt(prompt(widget))
