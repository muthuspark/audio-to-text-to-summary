import logging
import os
import tempfile

import openai
from dotenv import dotenv_values
from flask import Flask, request
from pydub import AudioSegment

from pipelines import diarization_pipeline, audio_transcription_pipeline
from util import random_name, is_mp3, is_wav, combine_same_successive_speaker_dialogues

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

config = dotenv_values(".env")

# API key does not need to be valid
openai.base_url = config.get("OPEN_AI_BASE_URL")
openai.api_key = config.get("OPEN_AI_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("FLASK_SECRET_KEY")


@app.errorhandler(Exception)  # Catches all exceptions
def handle_all_errors(error):
    error_message = getattr(error, 'message', str(error))  # Handle potential lack of 'message' attribute
    return f"An error occurred! Details: {error_message}", 500


def convert_mp3_to_wav(input_mp3_file):
    """
    This function converts an MP3 audio file to a WAV audio file.

    Args:
        input_mp3_file (str): Path to the MP3 file to be converted.
    """
    # Load the MP3 file using the AudioSegment from pydub library
    audio = AudioSegment.from_mp3(input_mp3_file)

    # Export the loaded audio to WAV format using the export method
    # and specifying the desired format ("wav") in the output filename
    output_wav_file = os.path.join(tempfile.gettempdir(), f"{random_name()}.wav")
    audio.export(output_wav_file, format="wav")
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


def split_audio_and_transcribe(input_wav_file_path, tracks):
    # Load the audio file
    audio = AudioSegment.from_file(input_wav_file_path)
    # Split the audio based on timestamps
    dialogues = []
    tracks = combine_same_successive_speaker_dialogues(tracks)
    for track in tracks:
        # Extract the segment
        segment = audio[track['start']:track['end']]
        temp_wav_file = os.path.join(tempfile.gettempdir(), f"{random_name()}.wav")
        segment.export(temp_wav_file, format="wav")
        logging.debug(f'Created a temporary file  {temp_wav_file}')
        try:
            result = audio_transcription_pipeline(temp_wav_file,
                                                  generate_kwargs={"task": "transcribe", "language": "english"})
            text = result["text"]
            audio_transcription_pipeline.call_count = 0
            dialogues.append(f"{track['speaker']}:{text}")
        except:
            print("found a very short or malformed audio")
            continue
        finally:
            # remove the temporarily created file
            os.remove(temp_wav_file)
    return dialogues


def chat_with_llm(message):
    completion = openai.chat.completions.create(model="mistral-openorca",
                                                messages=[{"role": "user", "content": message, }, ], )
    return completion.choices[0].message.content


@app.route('/summarize_conversation', methods=['POST'])
def summarize_conversation():
    json_data = request.json
    audio_file_path = json_data['audio_file_path']
    logging.debug(f'Started processing summarization for {audio_file_path}')
    if is_mp3(audio_file_path):
        audio_file_path = convert_mp3_to_wav(audio_file_path)
        logging.debug(f'Converted mp3 to wav and stored at {audio_file_path}')

    if is_wav(audio_file_path):
        logging.debug(f'Started Diarization of {audio_file_path}')
        tracks = audio_diarization(audio_file_path)
        logging.debug(f'Diarization completed successfully')
        logging.debug(f'Started transcribing process')
        dialogues = split_audio_and_transcribe(audio_file_path, tracks)
        logging.debug(f'Transcribing complete')
        dialogues = '\n'.join(dialogues)
        message = f"Give me a long summary of this conversation \n {dialogues}"
        return {'summary': chat_with_llm(message), 'transcript': dialogues}

    logging.debug(f'Unknown file format')
    return "error"


@app.route('/chat_with_llm', methods=['POST'])
def post_chat_with_llm():
    json_data = request.json
    message = json_data['message']
    return {'response': chat_with_llm(message), 'message': message}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get("SERVICE_PORT"))
