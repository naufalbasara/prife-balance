import logging, re
logging.basicConfig(filename='../running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')
from crontab import CronTab
from utils.utils import get_user

if __name__ == '__main__':
    current_user = get_user()
    cron = CronTab(user=f'{current_user}')

    for job in cron.find_comment(re.compile(r'^prife')):
        cron.remove(job)

    cron.write_to_user(current_user)