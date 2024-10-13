from loguru import logger
from check_info.telegram_dict import add_telegram_message
from files_work.pickle_files import dump_pickle, load_pickle
from telegram.send_message_to_telegram import send_telegram_message, SendTelegramMessage


def check_article_status(today_filename, path_to_pickle_folder, article_dict):
    dump_pickle(path_to_pickle_folder, today_filename, article_dict)
    article_dict = load_pickle(path_to_pickle_folder, today_filename)
    # logger.info(article_dict)
    article_dict.setdefault('telegram_info', [])
    # logger.info(article_dict)

    for article_name, article_status in article_dict.items():
        print(article_name, article_status)
        try:
            # if article_status == '***&site':
            if article_status == '***&site' or article_status == 'RRR&site':
                if article_name not in article_dict['telegram_info']:
                    logger.info(f'New message was sent \n{article_name} - {article_status}')
                    send_telegram_message(f'{article_name} - {article_status}')
                    article_dict = add_telegram_message(article_dict, article_name)
                    article_dict[article_name] = article_status
                    dump_pickle(path_to_pickle_folder, today_filename, article_dict)
                else:
                    logger.info(f'The message was sent earlier {article_name} - {article_status}')
            dump_pickle(path_to_pickle_folder, today_filename, article_dict)

            # else:
            #     logger.info("No changes in pickle file")
        except KeyError as key:
            # send_telegram_message(f'No such line in RDK - {key}')
            SendTelegramMessage(f'No such line in RDK - {key}').send_message()
            logger.error(f'No such line in RDK - {key}')
        # dump_pickle(path_to_pickle_folder, today_filename, article_dict)
        # logger.info(article_dict)


if __name__ == '__main__':
    check_article_status('04-03-2024', "../Pickle_files",
                         {'Юбилей первого выступления Утесова СТАВИМ ЗАВТРА': '***&site'})
