import os
import csv
from base import BASE_URL
import requests
from requests.structures import CaseInsensitiveDict
import aiohttp
import asyncio
import json


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

    default_payload['LatitudeMax'] = int(theLat) + 0.2
    default_payload['LatitudeMin'] = int(theLat) - 0.2
    default_payload['LongitudeMax'] = int(theLong) + 0.2
    default_payload['LongitudeMin'] = int(theLong) - 0.2

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
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'visid_incap_2269415=cM6CqGZKTkm5MJLmj7P7M0NUvWQAAAAAQUIPAAAAAADPZhsMQaZ7Ruc+dXg8rDgc; nlbi_2269415=7nBaQOv+Hg0/4JEqZ/XrMgAAAAATXPlX632g1G8IQIaGeTts; incap_ses_8078_2269415=ZqPoAV5eEVqcsugF99IacENUvWQAAAAANUl5dczSLu61HOdRbBpH9g==; nlbi_2269415_2147483392=f66ZdYRYGBWLhJNJZ/XrMgAAAAC0h/M0BSkVdIEilUcqVQBZ; reese84=3:/uPPEmA7bgT2xFJIG6VW6Q==:gkhsxvECgzDM9Qf76i+NINgBcolLHsbFNP69qGdY+FOm3rkhLya+2bLdMvt/C5WAaGgASUkQ+yxWK4i2TlY+bInZaNTeGRWksTGKHjR0s3Ac+sHNxF9vwW3MRjeS3hAMt81jtKdiJjJLD85VTAHpKhHMDTYl2UOlNKeEdCmd4gmEvezKlhVsOcAE+2XRJEsf9vhBqGuEtHbiKrE1lS6g+rScaHb0wvjLXMCXlD/xkGnndOyyKjJVMEH51MMDQiOP1mab38ZCvpgeFpU+ymSU6JXH2l8vCUaxuJob9qJm47TNQv1HLZ+ydDSDc95FanTr0Ba3Q1k2MPNDgMK6Owhju5Ps1vU0rovvTSTnS+16/Qi7syozVHuZqlGvoX+GL9DE81UQlYLw4c9/ZsmP949d01lhmGCP7BRBmDJWHNNivb2M4Izk2/Kl0xwYMXJwtXhYO1rVGGbKvBD7Obvu6xXSsQ==:Ha29iZXbUcTvxgm/xy2eW8NKEV6SoE2n5TGcyYJapDE=; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; ASP.NET_SessionId=4dk4yrekigcqxsxo2jn4ia2x; visid_incap_2271082=vnxzynlTTN+y2tPQOC8E+V1UvWQAAAAAQUIPAAAAAAA5VRlgXPK2L55jaYEZNa0g; nlbi_2271082=3sQkDJAz5A+zFB6pVPrQ3QAAAAAeDobWuSuE1lwl3tijX615; incap_ses_8078_2271082=/i0kW3n2ZRvZ7egF99IacF1UvWQAAAAA3UXJZhqvMRKxzXbCJ64rGg==',
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
                response_data = await response.text()
            else:
                print("Request failed")
                print("Response status code:", response.status)
                response_text = await response.text()
                print("Response text:", response_text)

if __name__ == "__main__":
    csv_file_path = "output.csv"  # Replace with the actual path to your output.csv file
    asyncio.run(realtor_request())
