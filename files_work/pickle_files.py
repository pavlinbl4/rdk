import os
import pickle
import re
from typing import BinaryIO

from loguru import logger


def file_name(pickle_file):
    return re.findall(r'\d{2}-\d{2}-\d{4}', pickle_file)[0]


def load_pickle(path_to_pickle_folder, pickle_file_name):
    try:
        file_path = os.path.join(path_to_pickle_folder, f'{pickle_file_name}.pickle')
        with open(file_path, 'rb') as articles:
            article_dict = pickle.load(articles)
        return article_dict
    except FileNotFoundError as file_error:
        logger.error(f"File not found: {file_error}")
        return None


def dump_pickle(path_to_pickle_folder: str, pickle_file_name: str, article_dict = None) -> None:
    logger.info(f'{path_to_pickle_folder = }')
    if article_dict is None:
        article_dict = {}
    file_path = os.path.join(path_to_pickle_folder, f'{pickle_file_name}.pickle')
    f: BinaryIO
    with open(file_path, 'wb') as f:  # f is of type BinaryIO
        pickle.dump(article_dict, f)
        logger.info(f"File {pickle_file_name} updated")


def delete_old_pickle(today_filename: str, path_to_pickle_folder: str) -> None:
    for file in os.listdir(path_to_pickle_folder):
        if file.endswith('pickle'):
            pickle_file = os.path.join(path_to_pickle_folder, file)
            if file != f'{today_filename}.pickle':
                os.remove(pickle_file)
                logger.info(f"File {file} removed")
