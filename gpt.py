from openai import OpenAI
from jproperties import Properties


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
                "role": "user",
                "content": prompt_text,
            }
        ],
        model=get_openai_property("model"),
    )
    response = chat_completion.choices[0].message.content
    response = list(filter(None, response.splitlines()[1:]))
    print_response(response)
    return response


def prompt(widget):
    return f"""I wrote Python method that takes as input description of actions 
    and performs the actions using Selenium WebDriver. Current web page contains 
    {widget.name} widget. Widget description: {widget.base_description} 
    Properties of this particular widget: {widget.widget_specific_description} 
    I want you to generate one test scenario for this specific widget that I 
    can use as input for my Python method. Keep test steps as simple, short as 
    possible. Per one step verify only one component. Use terms from widget 
    description. Always wrap widget component names inside single quotes. 
    As user actions use these verbs: click, verify. As 
    verification verbs use these: displayed, not displayed, present, not 
    present, page is opened, <component name> text is, <component name> text 
    contains. Use verbs that are concrete, not ambiguous or abstract. 
    No need to mention opening the webpage as a first step. 
    'page is opened' is not a component"""


def generate_scenario_for(widget):
    return request_gpt(prompt(widget))


def print_prompt(widget):
    print(f'prompt: {prompt(widget)}')


def print_response(response):
    print("\n")
    for line in response:
        print(line)
