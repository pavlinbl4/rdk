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
