def check_tg_message(article_dict: dict,):
    all_messages = article_dict.get('telegram_info', [])
    print(all_messages)
    print(article_dict)


def add_telegram_message(article_dict: dict, message: str):
    article_dict.setdefault('telegram_info', [])
    article_dict['telegram_info'].append(message)
    return article_dict


if __name__ == '__main__':
    print(add_telegram_message({1: 2}, 'message'))
    check_tg_message({1: 2}, 'fffff')
