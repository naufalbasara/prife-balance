import logging, datetime, json, os, sys, re
logging.basicConfig(level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')

from utils.scraper import fetch_prayertime
from utils.utils import get_pardir
from crontab import CronTab

if __name__ == '__main__':
    """
        Scheduler script to update the data daily (After user booting with cron job) by scraping the data source
    """

    # Get the data from data source and store it in data.json
    prayertime_data = fetch_prayertime(type='daily')
    fp = os.path.join(get_pardir(), 'data.json')
    
    with open(fp, 'w') as to_write:
        json.dump(prayertime_data, to_write)

    # Update cron job
    ### code here

    