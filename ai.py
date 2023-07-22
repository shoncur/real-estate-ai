import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def process_user_message(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "The user is going to give you the things they look for in a property. You are going to take this input, and display to me the # of bedroom's they want, # of bathroom's they want, the square footage of the property, and the location. Give me all of the fields that they supply, it does not need to be all four."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    ai_response = response['choices'][0]['message']['content']

    # Check if the AI has given the signal that it received the required data
    if "Thank you for providing the data." in ai_response:
        # Save the table data to a JSON file
        table_data = {}
        rows = ai_response.split('\n')
        for row in rows:
            if ':' in row:
                key, value = row.split(':', 1)
                table_data[key.strip()] = value.strip()

        # Save the table data to a JSON file
        with open('output.json', 'w') as json_file:
            json.dump(table_data, json_file)

    return ai_response
