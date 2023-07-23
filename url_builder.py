import os
import csv
from base import BASE_URL
import requests
from requests.structures import CaseInsensitiveDict

def get_long_lat(location):

    url = "https://api.geoapify.com/v1/geocode/search?text=" + location + "&apiKey=" + os.getenv("GEOLOCATION_API_KEY")

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    print(resp.status_code)
    print(resp.json())

    theLong = resp.json()['features'][0]['properties']['lon']
    theLat = resp.json()['features'][0]['properties']['lat']

    return {'long': theLong, 'lat': theLat}

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

if __name__ == "__main__":
    csv_file_path = "output.csv"  # Replace with the actual path to your output.csv file
    data = read_csv_file(csv_file_path)
    res = list(map(str.strip, data.split(',')))
    location = res.index('Location')
    long_lat = get_long_lat(res[location + 1])
    search_url = build_search_url(data)
    print("Search URL:", search_url)
