# pip install python-dotenv
# pip install webdriver-manager


from dotenv import load_dotenv
import os
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from time_tools.time_zone import get_city_time
import re
from loguru import logger

logger.disable("get_today_link")

service = Service(GeckoDriverManager().install())
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(service=service, options=options)


def find_article_status(article_status='GetImage.axd?kind=WF&key=E&site=RDK2SPB'):
    re_pattern = r'(?<=key=).*(?==RDK2SPB)'
    match = re.search(re_pattern, article_status)
    return match.group(0) if match else None


def save_html_page(page_name):
    page_source = driver.page_source
    with open(f"{page_name}.html", "w", encoding="utf-8") as f:
        f.write(page_source)


def find_date(str_with_date='№24 Пн, 25.02.24'):
    re_pattern = r'\d{2}\.\d{2}\.\d{2}'
    return re.findall(re_pattern, str_with_date)[0]


def get_today_link(all_spans):
    today = get_city_time('Europe/Moscow').strftime("%d.%m.%y")
    # today = '04.03.24'
    logger.info(today)
    for span in all_spans:
        if find_date(span.text) == today:
            today_link = span.get_attribute('href')
            logger.info(f"{today_link =  } ")
            return today_link


def get_spans():
    load_dotenv()
    rdk_logging = os.environ.get('rdk_logging')

    try:
        driver.get(rdk_logging)
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы: {e}")
        driver.quit()
        raise


    # driver.get('https://rdk.spb.kommersant.ru:9443/rdk2/?p=RDK2SPB,NODE:2353975')
    # driver.save_screenshot('rdk_page.png')

    # save page as html
    # save_html_page(driver, 'rdk_page.html')

    all_spans = driver.find_elements('xpath', '//span[@id="phList"]/a')
    # logger.info(f"{len(all_spans)}")
    return all_spans


def get_work_map(article_dict: dict):
    all_spans = get_spans()
    today_link = get_today_link(all_spans)
    driver.get(today_link)  # '//tr[@class="mapLO"][2]/td[6]/img'

    # save page as html
    # save_html_page(driver, 'rdk_today')

    work_map = driver.find_elements('xpath', '//tr[@class="mapLO"]')

    for x in range(1, len(work_map)):
        all_trs = work_map[x].find_elements('xpath', 'td')
        article_name = all_trs[0].text
        article_status = find_article_status(all_trs[5].find_element('xpath', 'img').get_attribute('src'))
        article_dict[article_name] = article_status
        logger.info(article_name)

    driver.quit()

    return article_dict


if __name__ == '__main__':
    get_work_map({'Юбилей первого выступления Утесова СТАВИМ ЗАВТРА': 'V&site'})
