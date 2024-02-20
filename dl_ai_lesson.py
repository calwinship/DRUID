import openai
from dotenv import load_dotenv

load_dotenv()

llm_model = "gpt-3.5-turbo"


def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    if response is not None:
        print('it worked')
        print(response.choices[0].message.content)
        return response #.choices[0].message.content
    else:
        print('it did not')


if __name__ == "__main__":
    get_completion("What is 1+1?")