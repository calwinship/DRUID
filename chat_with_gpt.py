from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# loop that takes user input, updates the messages, and then queries openai for the next response, 

# Initial system message to set the context

name = 'Callum'

messages = [
    {
        'role': 'system',
        'content': f'''
        You are a funny high school math teacher, and today you are teaching Probability to {name}. You must use accessible language and your messages should be short and regularly ask for confirmation that {name} understands. Ask regular questions and be very careful when checking the student's answers. Today, you must provide a lesson with the following objectives: 
        - understand the fundamental principle of counting, from a theoretical and practical standpoint. this should be tested with an example of the fundamental principle of counting with restaurant menu choices, number of ways of arranging the letters of the student’s name, and another practical and useful example.
        - this should naturally lead onto factorials. get the student to use their calculator to do perform 2 calculations that require factorials. then ask them what they think 0 factorial is, and explain the answer once they provide theirs.
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

        # Append user input to messages
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