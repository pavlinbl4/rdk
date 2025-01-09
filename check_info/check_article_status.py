from loguru import logger
from check_info.telegram_dict import add_telegram_message
from files_work.pickle_files import dump_pickle, load_pickle
from telegram.send_message_to_telegram import send_telegram_message, SendTelegramMessage


def check_article_status(today_filename, path_to_pickle_folder, article_dict):
    # Сохраняем начальные данные
    dump_pickle(path_to_pickle_folder, today_filename, article_dict)
    article_dict = load_pickle(path_to_pickle_folder, today_filename)
    logger.info(f"{article_dict = }")
    article_dict.setdefault('telegram_info', [])

    updated = False  # Флаг, чтобы записывать файл только если есть изменения

    for article_name, article_status in article_dict.items():
        # Пропускаем служебный ключ
        if article_name == 'telegram_info':
            continue

        logger.info(f'Processing: {article_name} - {article_status}')

        try:
            if article_status in {'***&site', 'RRR&site'}:
                if article_name not in article_dict['telegram_info']:
                    logger.info(f'Sending new message: {article_name} - {article_status}')
                    send_telegram_message(f'{article_name} - {article_status}')
                    article_dict = add_telegram_message(article_dict, article_name)
                    updated = True  # Устанавливаем флаг, если данные изменились
                else:
                    logger.info(f'Message already sent: {article_name} - {article_status}')
            else:
                logger.info(f'No action required for: {article_name} - {article_status}')

        except KeyError as e:
            error_msg = f'No such line in RDK - {e}'
            logger.error(error_msg)
            SendTelegramMessage(error_msg).send_message()

    # Сохраняем изменения, если они есть
    if updated:
        dump_pickle(path_to_pickle_folder, today_filename, article_dict)
        logger.info('Pickle file updated.')

