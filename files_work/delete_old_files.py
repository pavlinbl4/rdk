import datetime
import os
from loguru import logger
from files_work.check_existing_file import create_dir


# Configure logger to delete files older than 1 day
def delete_old_log_files(logs_dir):
    now = datetime.datetime.now()
    threshold_time = (now - datetime.timedelta(days=1)).timestamp()
    logger.info(f"Current time: {now}, threshold time: {threshold_time}")

    for log_filename in os.listdir(logs_dir):
        log_path = os.path.join(logs_dir, log_filename)
        if not log_filename.endswith(".log"):
            logger.info(f"Skipping non-log file: {log_filename}")
            continue
        try:
            file_mtime = os.path.getmtime(log_path)
            if file_mtime < threshold_time:
                os.remove(log_path)
                logger.info(f"Deleted old log file: {log_filename}")
            else:
                logger.info(f"File {log_filename} is recent and was not deleted.")
        except Exception as e:
            logger.error(f"Error processing file {log_filename}: {e}")


if __name__ == '__main__':
    ex_logs_dir = create_dir('Logs')
    delete_old_log_files(ex_logs_dir)