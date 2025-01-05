import os
import pickle
import pytest
from unittest import mock

from files_work.pickle_files import file_name, load_pickle, dump_pickle, delete_old_pickle


@pytest.fixture
def mock_pickle_folder():
    """Fixture to create a mock pickle folder for testing."""
    with mock.patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = [
            '12-05-2024.pickle',
            '13-05-2024.pickle',
            '14-05-2024.pickle'
        ]
        yield "/mock/pickle/folder"


@pytest.fixture
def mock_article_dict():
    """Fixture to create a mock article dictionary."""
    return {"article_id": 1, "title": "Test Article"}


def test_file_name():
    """Test the `file_name` function."""
    pickle_file = "12-05-2024.pickle"
    assert file_name(pickle_file) == "12-05-2024"


def test_load_pickle(mock_pickle_folder, mock_article_dict):
    """Test the `load_pickle` function."""
    file_path = os.path.join(mock_pickle_folder, '12-05-2024.pickle')

    # Mock the open and pickle.load functions
    with mock.patch("builtins.open", mock.mock_open(read_data=pickle.dumps(mock_article_dict))):
        result = load_pickle(mock_pickle_folder, "12-05-2024")
        assert result == mock_article_dict

    # Test file not found
    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
        mocked_open.side_effect = FileNotFoundError
        result = load_pickle(mock_pickle_folder, "non_existing")
        assert result is None


def test_dump_pickle(mock_pickle_folder, mock_article_dict):
    """Test the `dump_pickle` function."""
    file_path = os.path.join(mock_pickle_folder, '12-05-2024.pickle')

    # Mock the open and pickle.dump functions
    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
        with mock.patch("pickle.dump") as mock_pickle_dump:
            dump_pickle(mock_pickle_folder, "12-05-2024", mock_article_dict)
            mock_pickle_dump.assert_called_once_with(mock_article_dict, mocked_open())


def test_delete_old_pickle(mock_pickle_folder):
    """Test the `delete_old_pickle` function."""
    today_filename = "12-05-2024"

    # Mock the os.remove function to avoid actual file deletion
    with mock.patch("os.remove") as mock_remove:
        delete_old_pickle(today_filename, mock_pickle_folder)
        mock_remove.assert_any_call(os.path.join(mock_pickle_folder, '13-05-2024.pickle'))
        mock_remove.assert_any_call(os.path.join(mock_pickle_folder, '14-05-2024.pickle'))
        assert mock_remove.call_count == 2