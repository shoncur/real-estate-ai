import os
import openai
import csv  # Import the csv module
from dotenv import load_dotenv
import subprocess

load_dotenv()
openai.api_key = os.getenv("API_KEY")

# Sending this to realtor.ca
default_payload = {
    'ZoomLevel': '5',
    'LatitudeMax': '0',
    'LongitudeMax': '0',
    'LatitudeMin': '0',
    'LongitudeMin': '0',
    'Sort': '6-D',
    'PropertyTypeGroupID': '1',
    'TransactionTypeId': '2',
    'PropertySearchTypeId': '0',
    'PriceMin': '1000000',
    'Currency': 'CAD',
    'RecordsPerPage': '10',
    'ApplicationId': '1',
    'CultureId': '1',
    'Version': '7.0',
    'CurrentPage': '1'
}

def process_user_message(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "The user is going to give you the things they look for in a property. You are going to take this input, and display to me the # of bedroom's they want, # of bathroom's they want, the square footage of the property, and the location. Give me all of the fields that they supply, it does not need to be all four. When you give me all of the fields, preface the response with 'Real estate data:'"
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
    if "Real estate data:" in ai_response:
        # Save the table data to a CSV file
        table_data = {}
        rows = ai_response.split('\n')
        for row in rows:
            if ':' in row:
                key, value = row.split(':', 1)
                key = key.strip().replace('-', '')
                table_data[key.strip()] = value.strip()

        # Save the table data to a CSV file
        with open('output.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in table_data.items():
                writer.writerow([key, value])

        # Call url_builder.py as a separate process and capture its output
        result = subprocess.run(["python", "url_builder.py"], capture_output=False, text=True)

        #url_builder_output = result.stdout.strip()

        # Append the url_builder output to the AI response
        #ai_response += "\n" + url_builder_output
    return ai_response
