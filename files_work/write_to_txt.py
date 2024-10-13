from time_tools.time_zone import get_city_time
from pathlib import Path


def write_to_txt(folder_name="TextS"):
    today_date = get_city_time('Europe/Moscow')
    (Path() / folder_name).mkdir(exist_ok=True)
    with open(f'{folder_name}/{today_date.strftime("%Y_%m_%d")}.txt', 'a') as text_file:
        text_file.writelines(f'{today_date.strftime("%Y:%m:%d - %H:%M")}\n')


if __name__ == '__main__':
    write_to_txt()
