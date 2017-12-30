import os

from datetime import datetime
from urllib.request import urlretrieve

from config.settings import GOOGLE_API_DRIVE_PARENT_ID
from google_drive.insert_file import insert_file

DIRECTORY = os.path.join('data', 'last_price', 'bitcoincharts')


def main():
    now = datetime.now()
    current_time = now.strftime('%Y%m%d%H%M%S')
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    url = 'http://api.bitcoincharts.com/v1/trades.csv?symbol=coincheckJPY'
    file_name = '{}.csv'.format(current_time)
    file_path = os.path.join(DIRECTORY, file_name)
    urlretrieve(url, file_path)
    insert_file(file_path,
                'bitcoincharts-coincheck-jpy-{}'.format(file_name),
                GOOGLE_API_DRIVE_PARENT_ID)


if __name__ == '__main__':
    main()
