import os
import openai
import csv
import json
from dotenv import load_dotenv
from url_builder import build_search_url
from url_builder import get_long_lat
from url_builder import default_payload
import subprocess
from test_json_info import info

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def filter_housing_list(json_dump):
    data = json.loads(json_dump)

    filtered_properties = []
    for result in data.get("Results", []):
        property_info = {
            "Bedrooms": result["Building"].get("Bedrooms", ""),
            "Bathrooms": result["Building"].get("BathroomTotal", ""),
            "SizeInterior": result["Building"].get("SizeInterior", ""),
            "PublicRemarks": result.get("PublicRemarks", "")
        }
        filtered_properties.append(property_info)

    for property_info in filtered_properties:
        print("Bedrooms:", property_info["Bedrooms"])
        print("Bathrooms:", property_info["Bathrooms"])
        print("SizeInterior:", property_info["SizeInterior"])
        print("PublicRemarks:", property_info["PublicRemarks"])
        print("-" * 30)

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

        #updated_payload = get_long_lat(table_data.get('Location', ''), default_payload)

        #realtor_url = build_search_url(updated_payload)

        # Call url_builder.py as a separate process and capture its output
        result = subprocess.run(["python", "url_builder.py"], capture_output=False, text=True)

        print(default_payload)

        #filter_housing_list(info)

        #url_builder_output = result.stdout.strip()

        # Append the url_builder output to the AI response
        #ai_response += "\n" + url_builder_output
    return ai_response
