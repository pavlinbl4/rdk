from browser.driver_job import get_work_map
from check_info.check_article_status import check_article_status
from files_work.check_existing_file import create_dir
from files_work.delete_old_files import delete_old_log_files
from files_work.pickle_files import delete_old_pickle, dump_pickle, load_pickle
from time_tools.time_zone import get_city_time
from loguru import logger
import os

logs_dir = create_dir('Logs')
logger.add(f'{logs_dir}/debug.log', rotation="10:00")


def get_article_status():
    # create today day string look like '28-02-2024'
    today_filename = get_city_time('Europe/Moscow').strftime("%d-%m-%Y")
    # today_filename = 'RDK'
    logger.info(today_filename)

    delete_old_log_files(logs_dir)

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

    # get information from RDK site
    try:
        article_dict = get_work_map(article_dict)
    except Exception as e:
        logger.error(f"Error while fetching work map: {e}")
        return
    logger.info(article_dict)

    check_article_status(today_filename, path_to_pickle_folder, article_dict)


if __name__ == '__main__':
    get_article_status()
