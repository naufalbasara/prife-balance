import logging, sys, os, json, re
logging.basicConfig(filename='../log/running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')
from crontab import CronTab
from utils.utils import get_pardir, get_user
from utils.notifications import Notifications

def install_reqs():
    try:
        os.chdir('..')
        os.system('python3 -m venv venv')
        os.system('venv/bin/python -m pip install -r requirements.txt')
        os.chdir('src')
        return True

    except Exception as error:
        logging.error(f'Failed to install requirements due to {error}')
        return False

if __name__ == '__main__':
    logging.info("User setup begin, fetching the data and setting all the cron jobs")
    installed_status = install_reqs()
    notification = Notifications()

    if installed_status == False:
        print("Failed to install requirements")
    else:
        # Get user input on city and do sanity check on input
        city_country = input("\nInput your city, country (e.g. 'Surabaya, Indonesia'): ")
        while re.match(r'[\w]+, [\w]+', city_country) == None:
            city_country = input("Please provide the correct input (e.g. 'Surabaya, Indonesia'): ")

        os.system(f'../venv/bin/python scheduler.py "{city_country}"')
        
        # Setup job to update the data daily at 9AM
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
                    prayer_job = cron.new(command=f'cd {pardir}/src && {pydir} {notifier} {prayer}-{time}', comment=f'prife-{prayer}', user=f'{current_user}')
                    prayer_job.setall(f'{minute} {hour} * * *')
                    prayer_job.enable()

                location = json.load(json_file)['Location']
                city, country = location['city'], location['country']
            
            # commit to write cron job(s)
            cron.write_to_user(user=current_user)
            print("\n[info]:\tcron jobs installed.")
            logging.info("User setup succeed")
            print("\nUser setup succeed.")

            notification.notify('', 'Setup succeed', '', f'Notifications will come out every prayer time in your location ({city}, {country})')

        except Exception as error:
            logging.error(f"User setup failed -> {error}")
            print(f"User setup failed -> {error}")