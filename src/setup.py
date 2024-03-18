import sys, os, json
from crontab import CronTab
from utils.utils import get_pardir, get_user

if __name__ == '__main__':
    # Setup job to update the data daily at 9AM
    current_user = get_user()
    cron = CronTab(user=f'{current_user}')
    job = cron.new(command='source ../venv/bin/activate; python scheduler.py', comment='prife-Prayer time weekly update', user=f'{current_user}')
    job.setall('0 9 * * 1')

    # get all the prayer data and set the cron job to each of them
    fp = os.path.join(get_pardir(), 'data.json')
    with open(fp, 'r') as json_file:
        jsobj = json.load(json_file)['Daily Schedule']
        for prayer, time in jsobj.items():
            hour, minute = time.split(":")
            prayer_job = cron.new(command=f'source ../venv/bin/activate; python notify.py {prayer}-{time}', comment=f'prife-{prayer}', user=f'{current_user}')
            prayer_job.setall(f'{minute} {hour} * * *')
            print('Prayer job valid: ', prayer_job.is_valid())
            prayer_job.enable()
            cron.write_to_user(user=current_user)

    print("JOBs")
    for job in cron:
        print(job)