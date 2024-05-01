import os
import random
import string
from dotenv import dotenv_values

config = dotenv_values(".env")


def random_name(k=8):
    """
    Generate a random string of length k
    :return: string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))


def get_file_extension(path):
    """
    This function extracts the file extension from a given path.

    Args:
        path (str): The path to the file.

    Returns:
        str: The file extension (e.g., ".txt", ".jpg"). An empty string if no extension is found.
    """
    return os.path.splitext(path)[1].lower()


def is_mp3(path):
    return 'mp3' in get_file_extension(path)


def is_wav(path):
    return 'wav' in get_file_extension(path)


def is_webm(path):
    return 'webm' in get_file_extension(path)


def get_filename_without_extension(path):
    """Gets the filename from a path without the extension.

    Args:
        path: The file path.

    Returns:
        The filename without the extension, or None if the path is empty or doesn't have an extension.
    """
    if not path:  # Check if the path is empty
        return None

    # Find the last dot (.) in the path
    dot_index = path.rfind(".")

    if dot_index == -1:  # No extension found
        return path

    # Return the filename by slicing from the beginning to the last dot
    return path[:dot_index]


def get_filename_without_path(path):
    """Gets the filename from a path without the full path.

    Args:
        path: The file path.

    Returns:
        The filename.
    """
    return os.path.basename(path)


def get_parent_directory(path):
    """Gets the parent directory from a path.

    Args:
        path: The file path.

    Returns:
        The parent directory path, or None if the path is empty or has no parent directory.
    """
    return os.path.dirname(path)


def get_path_in_wav_format(input_file_path):
    input_file_name = get_filename_without_path(input_file_path)
    output_wav_file_name = f"{get_filename_without_extension(input_file_name)}.wav"
    return os.path.join(config.get("UPLOAD_FOLDER"), output_wav_file_name)
