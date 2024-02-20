from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


name = 'Callum'


P1 = {

    "Question 1": {
      "text": "Find the two values of m for which |5 + 3m| = 11.",
      "Solution": {
        "Method 1": {
          "steps": [
            "Solve 5 + 3m = 11 to get m = 2.",
            "Solve 5 + 3m = -11 to get m = -16/3."
          ],
          "outcome": ["m = 2", "m = -16/3"]
        },
        "Method 2": {
          "steps": [
            "Square both sides and solve the resulting equation: (5 + 3m)^2 = 11^2.",
            "Expand and simplify to get 9m^2 + 30m - 96 = 0.",
            "Factor or use the quadratic formula to find m = -16/3, m = 2."
          ],
          "outcome": "m = -16/3 and m = 2",
        }
      },
      "Tags": ["Absolute Value", "Linear Equations", "Quadratic Equations", "Factoring", "Quadratic Formula"] ,
      
    }

  }


messages = [
    {
        'role': 'system',
        'content': f'''
        You are a maths teacher, and your job is to explain exam questions to students. give short and accessible answers. get the student to do the thinking and you are just there to supervise and check their answers.  
        '''
    }
]

def chat_with_openai(messages):
    while True:
        # Take user input
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Exiting chat.")
            break

        if user_input.lower() == 'question 1':
            messages.append({'role': 'user', 'content': f'ask me the question {P1["Question 1"]["text"]} and do not provide the answer. ask it like "here is the first question ..." the answer is {P1["Question 1"]["Solution"]["Method 2"]["outcome"]} but i do not want that or the solution yet'})
        elif user_input.lower() == 'solution':
            solution = P1["Question 1"]["Solution"]["Method 1"]["steps"] + P1["Question 1"]["Solution"]["Method 2"]["steps"]
            messages.append({'role': 'user', 'content': f'could you please try to explain the {user_input} to the question, use {" ".join(solution)} as a guide'} )

        else:
            messages.append({'role': 'user', 'content': user_input})

        # Get response from OpenAI
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3, 
            stream = True
        )


        if response is not None:
            ai_response = ''
            print("Assistant:")
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end='')
                    ai_response += chunk.choices[0].delta.content

            # Append assistant's response to messages for context in the next round
            messages.append({'role': 'assistant', 'content': ai_response})
            print(

            )
        else:
            print("No response from the assistant.")

if __name__ == "__main__":
    chat_with_openai(messages)