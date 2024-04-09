from utils.utils import pardir, get_user
import logging, json, os, sys, re
logging.basicConfig(filename=f'{pardir}/log/running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')

from utils.scraper import fetch_prayertime, get_location
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
    else:
        location = None
    
    # Get the data from data source and store it in data.json
    prayertime_data = fetch_prayertime(location=location, type='daily')
    fp = os.path.join(pardir, 'data.json')
    
    # Load data to json file
    with open(fp, 'w') as to_write:
        json.dump(prayertime_data, to_write)
        logging.info('Prayer time data updated to data.json')

    # Update CRON Jobs
    if len(sys.argv) == 1:
        current_user = get_user()
        cron = CronTab(user=f'{current_user}')

        for prayer, time in prayertime_data['Daily Schedule'].items():
            job = next(cron.find_comment(re.compile(f'^prife-{prayer}')))
            hour, minute = time.split(":")
            end = re.search(f'{prayer}-', job.command).end()
            job.command = job.command[:end] + time
            job.setall(f'{minute} {hour} * * *')
            job.enable()
        
        cron.write_to_user(user=current_user)
        logging.info('Prayer time data updated to cron job')