import logging, re
logging.basicConfig(filename='../log/running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')
from crontab import CronTab
from utils.utils import get_user

if __name__ == '__main__':
    """
    This script only removed prife cron jobs
    """
    current_user = get_user()
    cron = CronTab(user=f'{current_user}')

    for job in cron.find_comment(re.compile(r'^prife')):
        cron.remove(job)
        logging.info(f'{job} removed from cron')

    cron.write_to_user(current_user)
    logging.info('prife cron job removed.')
    print('[info]:\tprife cron job removed.')