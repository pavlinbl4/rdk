from pathlib import Path

def check_file(file_name: str) -> bool:
    script_dir = Path(__file__).parent
    file_path = script_dir / file_name
    return file_path.is_file()


def create_dir(folder_name: str) -> str:
    try:
        script_dir = Path(__file__).parent
        folder_path = script_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        return str(folder_path)
    except Exception as e:
        raise RuntimeError(f"Failed to create directory '{folder_name}': {e}")


if __name__ == '__main__':
    assert check_file('../requirements.txt') is True, "File 'requirements.txt' should exist."
    assert check_file('27-02-2024.pickle') is False, "File '27-02-2024.pickle' should not exist."
    print("All tests passed.")