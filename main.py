import os

from loguru import logger

from browser.driver_job import get_work_map
from check_info.check_article_status import check_article_status
from files_work.check_existing_file import create_dir
from files_work.pickle_files import delete_old_pickle, dump_pickle, load_pickle
from time_tools.time_zone import get_city_time

logs_dir = create_dir('Logs')
logger.add(f'{logs_dir}/debug.log', rotation="10:00", retention="3 days", compression="zip", encoding="utf-8")


def get_article_status():
    # create today day string look like '28-02-2024'
    today_filename = get_city_time('Europe/Moscow').strftime("%d-%m-%Y")
    # today_filename = 'RDK'
    logger.info(today_filename)

    # deleted_logs = delete_old_log_files(logs_dir)
    # logger.info(f"Deleted {deleted_logs} old log files from {logs_dir}.")

    # set folder to pickle files
    pickle_folder = 'Pickle_files'
    path_to_pickle_folder = create_dir(pickle_folder)
    # logger.info(f"{path_to_pickle_folder}")

    # delete old pickle file
    delete_old_pickle(today_filename, path_to_pickle_folder)

    # create new pickle file
    if not os.path.exists(f'{path_to_pickle_folder}/{today_filename}.pickle'):
        dump_pickle(path_to_pickle_folder, today_filename)

    article_dict = load_pickle(path_to_pickle_folder, today_filename)
    logger.info(article_dict)
    # get information from RDK site
    try:
        article_dict = get_work_map(article_dict)

    except Exception as e:
        logger.error(f"Error while fetching work map: {e}")
        return


    check_article_status(today_filename, path_to_pickle_folder, article_dict)


if __name__ == '__main__':
    get_article_status()
