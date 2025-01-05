import os

from files_work.check_existing_file import check_file, create_dir

def test_check_file_existing():
    assert check_file('../requirements.txt') is True


def test_check_file_non_existing():
    assert check_file('non_existing_file.txt') is False

def test_create_dir():
    # Создаем директорию в корне скрипта
    folder_name = 'TestFolder'
    folder_path = create_dir(folder_name)

    assert os.path.exists(folder_path)
    assert os.path.isdir(folder_path)

    # Удаляем созданную директорию после теста
    os.rmdir(folder_path)