import os
import csv
from base import BASE_URL
import requests
from requests.structures import CaseInsensitiveDict
import aiohttp
import asyncio


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

def get_long_lat(location):
    url = "https://api.geoapify.com/v1/geocode/search?text=" + location + "%" + "Canada" + "&apiKey=" + os.getenv("GEOLOCATION_API_KEY")

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    theLong = resp.json()['features'][0]['properties']['lon']
    theLat = resp.json()['features'][0]['properties']['lat']

    default_payload['LatitudeMax'] = int(theLat) + 0.01
    default_payload['LatitudeMin'] = int(theLat) - 0.01
    default_payload['LongitudeMax'] = int(theLong) + 0.01
    default_payload['LongitudeMin'] = int(theLong) - 0.01

    return default_payload

def read_csv_file(file_path):
    data = {}
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            key = row[0]
            value = row[1]
            data[key] = value
    return data

def build_search_url(data):
    search_params = []

    # Check if the required fields are present in the data
    if 'Number of bedrooms' in data:
        search_params.append(f"bedrooms={data['Number of bedrooms']}")
    if 'Number of bathrooms' in data:
        search_params.append(f"bathrooms={data['Number of bathrooms']}")
    if 'Square footage' in data:
        search_params.append(f"sqft={data['Square footage']}")
    if 'Location' in data:
        search_params.append(f"location={data['Location']}")

    # Combine the search parameters into the URL
    if search_params:
        search_url = BASE_URL + "&".join(search_params)
    else:
        search_url = BASE_URL

    return search_url

async def realtor_request():
    url = BASE_URL
    data = read_csv_file(csv_file_path)
    payload = get_long_lat(data['Location'])

    headers = {
    'authority': 'api2.realtor.ca',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://www.realtor.ca',
    'referer': 'https://www.realtor.ca/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            if response.status == 200:
                # The request was successful
                print("Request successful")
                response_data = await response.json()
                print("Response:", response_data)  # Get the response data in JSON format
            else:
                print("Request failed")
                print("Response status code:", response.status)
                response_text = await response.text()
                print("Response text:", response_text)

if __name__ == "__main__":
    csv_file_path = "output.csv"  # Replace with the actual path to your output.csv file
    asyncio.run(realtor_request())
