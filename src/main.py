from utils.scraper import fetch_prayertime
from utils.scraper import get_location
from mac_notifications import client
from pprint import pprint

import datetime, logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

if __name__ == '__main__':
    location_dict = get_location('surabaya', 'indonesia')

    pprint(fetch_prayertime(location=location_dict, type='daily'))


    # client.create_notification(
    #     title='Testing',
    #     subtitle='Hello world!'
    # )