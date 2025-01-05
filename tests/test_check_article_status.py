import pytest
from unittest.mock import patch, MagicMock

from check_info.check_article_status import check_article_status


@pytest.fixture
def mock_pickle_data():
    return {'Юбилей первого выступления Утесова СТАВИМ ЗАВТРА': '***&site'}


@pytest.fixture
def mock_path_and_filename():
    return "test_file.pickle", "test_folder"


@patch("check_info.check_article_status.dump_pickle")
@patch("check_info.check_article_status.load_pickle")
@patch("check_info.check_article_status.send_telegram_message")
@patch("check_info.check_article_status.add_telegram_message")
def test_check_article_status_new_message(
    mock_add_telegram_message,
    mock_send_message,
    mock_load_pickle,
    mock_dump_pickle,
    mock_pickle_data,
    mock_path_and_filename,
):
    today_filename, path_to_pickle_folder = mock_path_and_filename

    # Настраиваем заглушки
    mock_load_pickle.return_value = mock_pickle_data
    mock_add_telegram_message.return_value = {
        **mock_pickle_data,
        "telegram_info": ["Юбилей первого выступления Утесова СТАВИМ ЗАВТРА"],
    }

    # Вызов функции
    check_article_status(today_filename, path_to_pickle_folder, mock_pickle_data)

    # Проверяем, что сообщение отправилось
    mock_send_message.assert_called_once_with(
        "Юбилей первого выступления Утесова СТАВИМ ЗАВТРА - ***&site"
    )

    # Проверяем, что pickle был обновлен
    mock_dump_pickle.assert_called_with(
        path_to_pickle_folder,
        today_filename,
        {
            **mock_pickle_data,
            "telegram_info": ["Юбилей первого выступления Утесова СТАВИМ ЗАВТРА"],
        },
    )


# @patch("check_info.check_article_status.dump_pickle")
# @patch("check_info.check_article_status.load_pickle")
# @patch("check_info.check_article_status.send_telegram_message")
# def test_check_article_status_message_already_sent(
#     mock_send_message,
#     mock_load_pickle,
#     mock_dump_pickle,
#     mock_pickle_data,
#     mock_path_and_filename,
# ):
#     today_filename, path_to_pickle_folder = mock_path_and_filename
#
#     # Настраиваем заглушки
#     mock_load_pickle.return_value = {
#         **mock_pickle_data,
#         "telegram_info": ["Юбилей первого выступления Утесова СТАВИМ ЗАВТРА"],
#     }
#
#     # Вызов функции
#     check_article_status(today_filename, path_to_pickle_folder, mock_pickle_data)
#
#     # Проверяем, что сообщение НЕ отправилось
#     mock_send_message.assert_not_called()
#
#     # Проверяем, что pickle не был обновлен
#     mock_dump_pickle.assert_not_called()



# @patch("check_info.check_article_status.dump_pickle")
# @patch("check_info.check_article_status.load_pickle")
# @patch("check_info.check_article_status.send_telegram_message")
# def test_check_article_status_key_error(
#     mock_send_telegram_message,
#     mock_load_pickle,
#     mock_dump_pickle,
#     mock_pickle_data,
#     mock_path_and_filename,
# ):
#     today_filename, path_to_pickle_folder = mock_path_and_filename
#
#     # Настраиваем заглушки
#     mock_load_pickle.side_effect = KeyError("Test Error")
#
#     # Вызов функции
#     check_article_status(today_filename, path_to_pickle_folder, mock_pickle_data)
#
#     # Проверяем, что SendTelegramMessage был вызван
#     mock_send_telegram_message.assert_called_once_with("No such line in RDK - Test Error")