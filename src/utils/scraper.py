import requests,time,logging,re,datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

def get_location(city: str, country: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        logging.info(f'Getting ({city}, {country}) location details')
        driver.get(f'https://www.google.com/maps/place/{city} {country}')
        time.sleep(5)
        current_url = driver.current_url
        start,end = re.search(r'@(\-|\+|\s|[0-9.])+,(\-|\+|\s|[0-9.])+', current_url).span()
        coordinates = current_url[start+1:end].split(',')

        location = {
            'city': city,
            'coordinates': {
                'latitude': coordinates[0],
                'longitude': coordinates[1],
            },
            'country': country
        }
    except Exception as error:
        logging.error(f'Failed to get data due to:\n\t{error}')

    return location

def fetch_prayertime(location: dict, type: str):
    """
    Type determines how we get the data
    daily: Fetch prayer time data at specified date
    full_month: Fetch prayer time data for the whole month
    """

    fetch_time = datetime.datetime.now()
    current_date = fetch_time.strftime("%d-%m-%Y")

    endpoint_by_type = {
        'daily': f'https://api.aladhan.com/v1/timings/{current_date}?latitude={location["coordinates"]["latitude"]}&longitude={location["coordinates"]["longitude"]}&method=20',
        'full_month': f'https://api.aladhan.com/v1/calendar/{fetch_time.year}/{fetch_time.month}?latitude={location["coordinates"]["latitude"]}&longitude={location["coordinates"]["longitude"]}&method=20'
    }

    endpoint = endpoint_by_type[type]
    header = {
        'Accept':'text/html,application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        logging.info(f'Fetching prayer time at {location["city"]},{location["country"]} ({location["coordinates"]["latitude"]}, {location["coordinates"]["longitude"]}) on {current_date}')
        response = requests.get(endpoint, headers=header)
        data = response.json()['data']
    except Exception as error:
        logging.error(f'Failed to fetch due to:\n\t{error}')

    return data