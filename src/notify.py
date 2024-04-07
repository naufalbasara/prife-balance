from utils.utils import pardir
import logging, time, json, sys
logging.basicConfig(filename=f'{pardir}/log/running.log', filemode='a', level=logging.INFO, format=' %(asctime)s -  %(levelname)s:  %(message)s')

from utils.notifications import Notifications


if __name__ == '__main__':
    notification = Notifications('mac')
    name, pray_time = sys.argv[1].split('-')
    try:
        with open(f'{pardir}/data.json') as json_file:
            jsobj = json.load(json_file)
            notification.notify('', 'Pray Reminder', '', f'It\'s {name} time ({pray_time}) in {jsobj["location"]["city"]} and surrounding areas')
            logging.info(f"{name} ({pray_time}) Notification Success")
    except:
        logging.error(f'{name} ({pray_time}) Notification Failed')