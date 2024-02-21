from openai import OpenAI

openAI_token = "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"
model = "gpt-3.5-turbo"


def request_gpt(prompt):
    client = OpenAI(api_key=openAI_token)
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
    return f"""I wrote JAVA method that takes as input description of actions 
    and performs the actions using Selenium WebDriver Current web page contains 
    {widget.name} widget. Widget description: {widget.description} I want you 
    to generate one test scenario for this widget that I can use as input for 
    my JAVA method. Keep test steps as simple, short as possible. Use terms 
    from widget description. As user actions use set of these verbs: click, 
    open, close, verify, check. As verification verbs use these set: displayed, 
    not displayed, present, not present, other verbs that are concrete, not 
    ambiguous or abstract.
    No need to mention opening the webpage as a first step."""


def generate_scenario_for(widget):
    return request_gpt(prompt(widget))
