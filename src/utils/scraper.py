import requests,time,logging,re,datetime,json,os

from selenium import webdriver
from utils.utils import get_pardir

def get_location(city: str, country: str):
    "Getting coordinates from provided city and country"
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
        
        logging.info(f'Fetched data details, returned a dictionary')
    except Exception as error:
        logging.error(f'Failed to get data details due to:\n\t{error}')

    return location

def fetch_prayertime(location:dict=None, type:str='daily'):
    """
    Type determines how we get the data
    daily: Fetch prayer time data at specified date
    full_month: Fetch prayer time data for the whole month
    """

    fetch_time = datetime.datetime.now()
    current_date = fetch_time.strftime("%d-%m-%Y")

    if location == None:
        # If location none, get the data from data.json and assign to location variable
        try:
            with open(os.path.join(get_pardir(), 'data.json'), 'r') as json_file:
                location = json.load(json_file)['location']
        except:
            logging.error('data.json doesn\'t exist')

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
        data = response.json()['data']['timings']
        data = {
            'location': location,
            f'Daily Schedule ({current_date})': data
        }
    except Exception as error:
        logging.error(f'Failed to fetch due to:\n\t{error}')

    return data