import os
import random
import string


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


def combine_same_successive_speaker_dialogues(tracks):
    """
    Combines successive dialogues spoken by the same speaker into a single sequence.

    Args:
        tracks (list): A list of dictionaries representing speech tracks. Each dictionary should have keys
                       'speaker', 'start', and 'end' representing the speaker's name, start time of speech,
                       and end time of speech respectively.

    Returns:
        list: A list of dictionaries representing combined speech sequences with the same speaker.
              Each dictionary contains keys 'speaker', 'start', and 'end' representing the speaker's name,
              start time of the combined speech sequence, and end time of the combined speech sequence respectively.
    """
    speech_sequences = []

    # Iterate through each track in the provided list
    for track in tracks:
        # If there are no speech sequences yet, add the current track as a new sequence
        if len(speech_sequences) == 0:
            speech_sequences.append(track)
        # If the speaker of the current track matches the speaker of the last track in the sequences list,
        # extend the end time of the last sequence to include the current track
        elif speech_sequences[-1]['speaker'] == track['speaker']:
            speech_sequences[-1]['end'] = track['end']
        # If the speaker of the current track is different from the speaker of the last track,
        # start a new speech sequence with the current track
        else:
            speech_sequences.append(track)

    return speech_sequences
