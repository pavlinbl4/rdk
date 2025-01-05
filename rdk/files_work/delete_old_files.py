# script to delete old files
import datetime
import os
from icecream import ic
from loguru import logger

from rdk.files_work.check_existing_file import create_dir

ic.disable()


# Configure logger to delete files older than 1 days
def delete_old_log_files(logs_dir):
    now = datetime.datetime.now()
    ic(now)
    ic(datetime.timedelta(days=1))
    ic((now - datetime.timedelta(days=1)).timestamp())
    ic(type(now - datetime.timedelta(days=1)))
    for log_filename in os.listdir(logs_dir):
        if (log_filename.endswith(".log") and
                os.path.getmtime(f'{logs_dir}/{log_filename}') < (now - datetime.timedelta(days=1)).timestamp()):
            os.remove(f'{logs_dir}/{log_filename}')
            logger.info(f"File  {log_filename} deleted")
        logger.info(f'File {log_filename} is fresh')


if __name__ == '__main__':
    ex_logs_dir = create_dir('Logs')

    delete_old_log_files(ex_logs_dir)
