import logging, json, os, sys
logging.basicConfig(filename='../log/running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')

from utils.scraper import fetch_prayertime, get_location
from utils.utils import get_pardir
from crontab import CronTab

if __name__ == '__main__':
    """
        Scheduler script to update the data daily (After user booting with cron job) by scraping the data source
    """
    city, country = (None,None)
    if len(sys.argv) > 1:
        try:
            city, country = [*map(lambda x:x.strip(), sys.argv[1].split(','))]
            location = get_location(city, country)
        except:
            print('[ERROR]: Please provide the right city and country input (e.g. \"Surabaya, Indonesia\")')
    
    # Get the data from data source and store it in data.json
    prayertime_data = fetch_prayertime(location=location, type='daily')
    fp = os.path.join(get_pardir(), 'data.json')
    
    with open(fp, 'w') as to_write:
        json.dump(prayertime_data, to_write)
        logging.info('Prayer time data updated to data.json')

    