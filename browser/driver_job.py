# pip install python-dotenv
# pip install webdriver-manager


import os
import re

from dotenv import load_dotenv
from loguru import logger
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from time_tools.time_zone import get_city_time
import time

logger.disable("get_today_link")


def create_driver():
    service = Service(GeckoDriverManager().install())
    options = FirefoxOptions()
    # options.add_argument("--headless")
    return webdriver.Firefox(service=service, options=options)


def find_article_status(article_status='GetImage.axd?kind=WF&key=E&site=RDK2SPB'):
    re_pattern = r'(?<=key=).*(?==RDK2SPB)'
    match = re.search(re_pattern, article_status)
    return match.group(0) if match else None


def find_date(str_with_date='№24 Пн, 25.02.24'):
    re_pattern = r'\d{2}\.\d{2}\.\d{2}'
    return re.findall(re_pattern, str_with_date)[0]


def get_today_link(all_spans):
    today = get_city_time('Europe/Moscow').strftime("%d.%m.%y")


    logger.info(today)
    for span in all_spans:
        # logger.info(f"{span.text = }")
        if find_date(span.text) == today:
            today_link = span.get_attribute('href')
            # logger.info(f"{today_link =  } ")
            # logger.info(f"Загружено {len(all_spans)} элементов.")
            logger.info(f"Сегодняшняя ссылка: {today_link}")
            return today_link


def get_spans(driver):
    load_dotenv()
    rdk_logging = os.environ.get('rdk_logging')

    try:
        driver.get(rdk_logging)
        driver.get('https://rdk.spb.kommersant.ru:9443/rdk2/?p=RDK2SPB,NODE:2353975')
        #  https://rdk.spb.kommersant.ru:9443/rdk2/?p=RDK2SPB,NODE:2353975
        time.sleep(3)
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы: {e}")
        driver.quit()
        raise

    all_spans = driver.find_elements('xpath', '//span[@id="phList"]/a')
    # logger.info(f"{len(all_spans)}")
    return all_spans


def get_work_map(article_dict: dict):
    driver = create_driver()
    try:
        all_spans = get_spans(driver)
        today_link = get_today_link(all_spans)
        driver.get(today_link)
        time.sleep(3)
        work_map = driver.find_elements('xpath', '//tr[@class="mapLO"]')

        logger.info(f"{len(work_map) = }")
        for x in range(1, len(work_map)):
            logger.info(f"{work_map[x] = }")
            all_trs = work_map[x].find_elements('xpath', 'td')
            logger.info(f'{all_trs = }')
            article_name = all_trs[0].text
            article_status = find_article_status(all_trs[5].find_element('xpath', 'img').get_attribute('src'))
            article_dict[article_name] = article_status
            logger.info(article_name)
    finally:
        driver.quit()

    return article_dict
