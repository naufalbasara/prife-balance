from utils.utils import get_pardir, get_user, message, pardir
import logging, sys, os, json, re, virtualenv
logging.basicConfig(filename=f'{pardir}/log/running.log', filemode='a', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s:  %(message)s')
from crontab import CronTab
from utils.notifications import Notifications

def install_reqs():
    pardir = get_pardir()
    try:
        virtualenv.cli_run([os.path.join(pardir, 'venv')])
        os.system(f'{pardir}/venv/bin/python -m pip -q install -r {pardir}/requirements.txt')
        return True

    except Exception as error:
        logging.error(f'Failed to install requirements due to {error}')
        return False

if __name__ == '__main__':
    logging.info("User setup begin, fetching the data and setting all the cron jobs")
    print("Installing virtual environment...")
    installed_status = install_reqs()
    print('virtual environment installed.. ', f'{message("SUCCESS")}' if installed_status else f'{message("FAILED")}')
    notification = Notifications()

    if installed_status == False:
        print("Failed to install requirements")
    else:
        # Get user input on city and do sanity check on input
        city_country = input("\n\t➡️Input your city, country (e.g. 'Surabaya, Indonesia'): ")
        while re.match(r'[\w]+, [\w]+', city_country) == None:
            city_country = input("\n\t➡️Please provide the correct input (e.g. 'Surabaya, Indonesia'): ")

        print("\nScraping location coordinates...")
        os.system(f'{pardir}/venv/bin/python {pardir}/src/scheduler.py "{city_country}"')
        # Setup job to update the data daily at 9AM
        current_user = get_user()
        pardir = get_pardir()
        print('Location scraped.. ', f'{message("SUCCESS")}' if os.path.exists(os.path.join(pardir, 'data.json')) else f'{message("FAILED")}')

        pydir = os.path.join(pardir, 'venv/bin/python')
        scheduler = os.path.join(pardir, 'src/scheduler.py')
        notifier = os.path.join(pardir, 'src/notify.py')

        try:
            print("Set up cron jobs to be installed locally...", end=' ')
            cron = CronTab(user=f'{current_user}')
            job = cron.new(command=f'cd {pardir}/src && {pydir} {scheduler}', comment='prife-Prayer time weekly update', user=f'{current_user}')
            job.setall('0 9 * * *')

            # get all the prayer data and set the cron job to each of them
            fp = os.path.join(pardir, 'data.json')
            with open(fp, 'r') as json_file:
                jsobj = json.load(json_file)
                prayer_time = jsobj['Daily Schedule']
                location = jsobj['location']

                for prayer, time in prayer_time.items():
                    hour, minute = time.split(":")
                    prayer_job = cron.new(command=f'cd {pardir}/src && {pydir} {notifier} {prayer}-{time}', comment=f'prife-{prayer}', user=f'{current_user}')
                    prayer_job.setall(f'{minute} {hour} * * *')
                    prayer_job.enable()
                
                city, country =location['city'], location['country']
            
            # commit to write cron job(s)
            cron.write_to_user(user=current_user)
            print('✅')
            print(f'\n[info]:\tcron jobs installed... {message("SUCCESS")}')
            logging.info("User setup succeed")

            notification.notify('', 'Setup succeed', '', f'Notifications will come out every prayer time in your location ({city}, {country})')

        except Exception as error:
            logging.error(f"User setup {message('FAILED')} -> {error}")
            print(f"User setup {message('FAILED')} -> {error}")