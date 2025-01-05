from loguru import logger

def check_tg_message(article_dict: dict):
    all_messages = article_dict.get('telegram_info', [])
    logger.info("All messages in telegram_info:", all_messages)
    logger.info("Full article_dict:", article_dict)


def add_telegram_message(article_dict: dict, message: str):
    article_dict.setdefault('telegram_info', [])
    article_dict['telegram_info'].append(message)
    return article_dict


if __name__ == '__main__':
    article = add_telegram_message({1: 2}, 'message')
    print("Updated article:", article)
    check_tg_message(article)