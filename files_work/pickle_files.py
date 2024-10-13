import pickle
import os
import re
from loguru import logger


def file_name(pickle_file):
    return re.findall(r'\d{2}-\d{2}-\d{4}', pickle_file)[0]


def load_pickle(path_to_pickle_folder, pickle_file_name):
    try:
        with open(f'{path_to_pickle_folder}/{pickle_file_name}.pickle', 'rb') as articles:
            article_dict = pickle.load(articles)
        return article_dict
    except FileNotFoundError as file_error:
        logger.error(file_error)


def dump_pickle(path_to_pickle_folder, pickle_file_name, article_dict=None):
    # logger.info(f'{path_to_pickle_folder = }')
    if article_dict is None:
        article_dict = {}
    with open(f'{path_to_pickle_folder}/{pickle_file_name}.pickle', 'wb') as f:
        pickle.dump(article_dict, f)
        # logger.info(f"file {pickle_file_name} updated")


def delete_old_pickle(today_filename: str, path_to_pickle_folder: str):
    for file in os.listdir(path_to_pickle_folder):
        if file.endswith('pickle'):
            pickle_file = os.path.join(path_to_pickle_folder, file)
            if file != f'{today_filename}.pickle':
                os.remove(pickle_file)
                logger.info(f"file {file} removed")


if __name__ == '__main__':
    # ic(load_pickle('/Volumes/big4photo/_PYTHON/@_EDICATION/OOP/rdk_cheker/Pickle_files', '28-02-2024'))
    e_dict = {'СКА СТАВИМ СРАЗУ': 'W&site',
              'невкосметика ставить немедля': 'W&site',
              'парнас ставить сразу ж': 'W&site',
              'рынок рекламы на утро': 'E&site',
              'театрал срочно в номер': 'W&site',
              'шевченко ставить тотчас': 'W&site'}
    dump_pickle('Pickle_files', '27-02-2024')

    # delete_old_pickle(path_to_pickle_folder='/Volumes/big4photo/_PYTHON/@_EDICATION/OOP/rdk_cheker/Pickle_files',
    #                   today_filename='28-02-2024')
