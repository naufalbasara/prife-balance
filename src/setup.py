import logging, sys, os, json, re
logging.basicConfig(filename='../running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')
from crontab import CronTab
from utils.utils import get_pardir, get_user

if __name__ == '__main__':
    # Setup job to update the data daily at 9AM
    logging.info("User setup begin, fetching the data and setting all the cron jobs")
    current_user = get_user()
    pardir = get_pardir()
    pydir = os.path.join(pardir, 'venv/bin/python')
    scheduler = os.path.join(pardir, 'src/scheduler.py')
    notifier = os.path.join(pardir, 'src/notify.py')

    try:
        cron = CronTab(user=f'{current_user}')
        job = cron.new(command=f'cd {pardir}/src && {pydir} {scheduler}', comment='prife-Prayer time weekly update', user=f'{current_user}')
        job.setall('0 9 * * *')

        # get all the prayer data and set the cron job to each of them
        fp = os.path.join(pardir, 'data.json')
        with open(fp, 'r') as json_file:
            jsobj = json.load(json_file)['Daily Schedule']
            for prayer, time in jsobj.items():
                hour, minute = time.split(":")
                prayer_job = cron.new(command=f'cd {pardir} && {pydir} {notifier} {prayer}-{time}', comment=f'prife-{prayer}', user=f'{current_user}')
                prayer_job.setall(f'{minute} {hour} * * *')
                prayer_job.enable()
        
        # commit to write cron job(s)
        cron.write_to_user(user=current_user)
        logging.info("User setup succeed")

    except Exception as error:
        logging.error(f"User setup failed -> {error}")