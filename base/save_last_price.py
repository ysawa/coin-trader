import os
import traceback

from bitflyer.api import BitflyerApi
from config.settings import GOOGLE_API_DRIVE_PARENT_ID
from google_drive.insert_file import insert_file

from time import sleep
from datetime import datetime


def save_last_price(api, directory):
    """

    :param base.BaseApi api:
    :param str directory:
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    past_date = None
    file_name = None
    while True:
        try:
            price = api.request_last_price()
            now = datetime.now()
            current_date = now.strftime('%Y%m%d')
            current_time = now.strftime('%Y%m%d%H%M%S')
            if past_date != current_date:
                if past_date is not None:
                    save_google_drive(file_name)
                past_date = current_date
            file_name = '{}.csv'.format(os.path.join(directory, current_date))
            csv_file = open(file_name, 'a')
            csv_file.write("{},{}\r\n".format(current_time, price))
            csv_file.close()
        except:
            print(traceback.format_exc())
            pass
        sleep(10)


def save_google_drive(file_name):
    insert_file(file_name, file_name.replace('/', '-'), GOOGLE_API_DRIVE_PARENT_ID)
