import openai

class LLMInterface:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_transformation_info(self, expression):
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Explain the transformation: {expression}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
