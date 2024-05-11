import http
import queue
import subprocess

from flask import Blueprint, jsonify
from flask import request
import os
import tempfile
import threading
from dotenv import dotenv_values

from llm import chat_with_llama
from pipelines import diarization_pipeline, audio_transcription_pipeline
from utilities.database import create_record, update_tracks, update_transcript, update_summary, get_by_id, get_all, \
    update_audio_file_name, is_summarizing_completed_for_recording, remove, update_recording_name
from utilities.request_queue import PersistentQueue
from utilities.util import is_mp3, is_wav, is_webm, get_path_in_wav_format
from pydub import AudioSegment
from logging_config import logger

summarize_routes_blueprint = Blueprint('summarize', __name__)

config = dotenv_values(".env")

summarization_request_queue = PersistentQueue(config.get("REQUEST_QUEUE_FILE"))


@summarize_routes_blueprint.route('/summarize_conversation', methods=['POST'])
def summarize_conversation():
    json_data = request.json
    audio_file_path = json_data['audio_file_path']
    return extract_summary_from_audio(audio_file_path)


@summarize_routes_blueprint.route('/get_summaries', methods=['POST'])
def get_summaries():
    return get_all()


@summarize_routes_blueprint.route('/remove_summary', methods=['POST'])
def remove_summary():
    json_data = request.json
    audio_file_name = json_data['audio_file_name']
    return remove(audio_file_name)


@summarize_routes_blueprint.route('/update_title', methods=['POST'])
def update_title():
    json_data = request.json
    audio_file_name = json_data['audio_file_name']
    recording_name = json_data['recording_name']
    return update_recording_name(audio_file_name, recording_name)


@summarize_routes_blueprint.route('/summarizing_completed', methods=['POST'])
def is_summarizing_completed():
    json_data = request.json
    recording_name = json_data['recording_name']
    status = is_summarizing_completed_for_recording(recording_name)
    if status:
        return jsonify({'message': 'Audio file summarization completed successfully'}), http.HTTPStatus.OK
    return jsonify({'message': 'Audio summarization in progress'}), http.HTTPStatus.NOT_MODIFIED


def summarize_conversation_worker():
    while True:
        if not summarization_request_queue.is_empty():
            try:
                audio_request = summarization_request_queue.get(block=False)
            except queue.Empty:
                # Queue is empty, continue to the next iteration
                continue
            audio_file_path = os.path.join(config.get("UPLOAD_FOLDER"), audio_request.data)
            if os.path.exists(audio_file_path):
                extract_summary_from_audio(audio_file_path, audio_request.recording_name)
                summarization_request_queue.task_done()


def extract_summary_from_audio(audio_file_path, recording_name):
    logger.debug(f'Started processing summarization for {audio_file_path}')
    audio_summary_record = create_record(audio_file_path, recording_name)
    audio_id = audio_summary_record.doc_id
    if is_mp3(audio_file_path):
        audio_file_path = convert_mp3_to_wav(audio_file_path)
        logger.debug(f'Converted mp3 to wav and stored at {audio_file_path}')
        update_audio_file_name(audio_id, audio_file_path)
    if is_webm(audio_file_path):
        audio_file_path = convert_webm_to_wav(audio_file_path)
        logger.debug(f'Converted mp3 to wav and stored at {audio_file_path}')
        update_audio_file_name(audio_id, audio_file_path)
    if is_wav(audio_file_path):
        if not audio_summary_record['tracks']:
            logger.debug(f'Started Diarization of {audio_file_path}')
            tracks = audio_diarization(audio_file_path)
            update_tracks(audio_id, tracks)
            audio_summary_record['tracks'] = tracks
            logger.debug(f'Diarization completed successfully')

        if not audio_summary_record['transcript']:
            logger.debug(f'Started transcribing process')
            transcript = split_audio_and_transcribe(audio_file_path, audio_summary_record['tracks'])
            logger.debug(f'Transcribing complete')
            transcript = '\n'.join(transcript)
            update_transcript(audio_id, transcript)
            audio_summary_record['transcript'] = transcript

        if not audio_summary_record['summary']:
            message = f"Give me a long summary of this transcript \n {audio_summary_record['transcript']}"
            summary = chat_with_llama(message)
            update_summary(audio_id, summary)

        return get_by_id(audio_id)
    logger.debug(f'Unknown file format')
    return "error"


def convert_mp3_to_wav(input_mp3_file):
    """
    This function converts an MP3 audio file to a WAV audio file.

    Args:
        input_mp3_file (str): Path to the MP3 file to be converted.
    """
    # Load the MP3 file using the AudioSegment from pydub library
    audio = AudioSegment.from_mp3(input_mp3_file)
    output_wav_file = get_path_in_wav_format(input_mp3_file)
    audio.export(output_wav_file, format="wav")
    os.remove(input_mp3_file)
    return output_wav_file


def convert_webm_to_wav(input_webm_file):
    """Converts a webm file to wav format using ffmpeg.

    Args:
        input_webm_file: Path to the input webm file.
    """
    output_wav_file = get_path_in_wav_format(input_webm_file)
    command = ['ffmpeg', '-i', input_webm_file, '-vn', '-acodec', 'pcm_s16le', output_wav_file]
    subprocess.run(command, check=True)
    os.remove(input_webm_file)
    return output_wav_file


def audio_diarization(input_wav_file):
    tracks = []
    # apply pretrained pipeline
    diarization = diarization_pipeline(input_wav_file)
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        # start=0.2s stop=1.5s speaker_0
        # start=1.8s stop=3.9s speaker_1
        # start=4.2s stop=5.7s speaker_0
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        # record the timestamps in milliseconds
        tracks.append({'start': round(turn.start, 1) * 1000, 'end': round(turn.end, 1) * 1000, 'speaker': speaker})
    return tracks


def transcribe_audio_segment(audio_segment):
    """
    Transcribe an audio segment using the audio_transcription_pipeline function.

    Args:
        audio_segment (AudioSegment): The audio segment to be transcribed.

    Returns:
        str: The transcribed text if successful, None otherwise.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file_path = temp_file.name
        try:
            audio_segment.export(temp_file_path, format="wav")
            result = audio_transcription_pipeline(temp_file_path,
                                                  generate_kwargs={"task": "transcribe", "language": "english"})
            transcription = result["text"]
            audio_transcription_pipeline.call_count = 0
            return transcription
        except Exception as e:
            logger.warning(f"Error transcribing audio segment: {e}")
            return None
        finally:
            os.remove(temp_file_path)


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


def split_audio_and_transcribe(input_wav_file_path, tracks):
    """
    Split an audio file into segments based on timestamps and transcribe each segment.

    Args:
        input_wav_file_path (str): The path to the input WAV file.
        tracks (list): A list of dictionaries containing speaker and timestamp information.

    Returns:
        list: A list of strings, each representing a dialogue in the format "speaker:transcription".
    """
    # Load the audio file
    audio = AudioSegment.from_wav(input_wav_file_path)

    # Split the audio based on timestamps and transcribe each segment
    dialogues = []
    tracks = combine_same_successive_speaker_dialogues(tracks)
    for track in tracks:
        # Extract the segment
        audio_segment = audio[track['start']:track['end']]
        transcription = transcribe_audio_segment(audio_segment)
        if transcription:
            dialogues.append(f"{track['speaker']}:{transcription}")
        else:
            logger.warning(f"Skipping malformed audio segment: {track}")

    return dialogues


worker_thread = threading.Thread(target=summarize_conversation_worker)
worker_thread.start()
