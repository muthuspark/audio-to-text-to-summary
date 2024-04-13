# Open-source Speech to Summary Pipeline

This project demonstrates a basic workflow for converting an audio dialogue to text and then summarizing it using
entirely open-source tools. While I am showcasing summarization with GeminiAI, any open-source Large Language Model (
LLM) can be integrated into this pipeline.

The steps involved are:

1. **Speech-to-Text Transcription:** Tools like Kaldi or Mozilla DeepSpeech can be used to convert the audio dialogue
   into a text transcript.
2. **Summarization with Open-Source LLM:** We can utilize GeminiAI or other open-source LLMs like BART or T5 to generate
   a concise summary of the text transcript.

This is a simple example, but it highlights the potential of building speech summarization pipelines using freely
available resources.

**Additional Considerations:**

* **Language Support:** Ensure the chosen speech-to-text and summarization tools support the language of the audio
  dialogue.
* **Accuracy:** Both speech recognition and summarization involve complexities that can impact accuracy. Consider
  techniques to improve these aspects.
* **Deployment:** The pipeline can be further developed for deployment as a web service or standalone application.

This revised version clarifies the purpose, mentions specific open-source tools, and suggests improvements for a more
robust pipeline.

### Pre-Requisites

Rename `.env_sample` to `.env` and fill in the variables following steps below.

1. Accept [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) user conditions
2. Create access token at [hf.co/settings/tokens](https://hf.co/settings/tokens)
3. Create a local LLM server using [localai](https://localai.io/basics/getting_started/). LocalAI act as a drop-in
   replacement REST API that’s compatible with OpenAI API specifications for local inferencing. If you wish to use
   openai you can simply switch to openai
    - I created my localai docker service using the below command
      ```
      docker run -p 8080:8080 --gpus all localai/localai:v2.12.1-cublas-cuda12-core mistral-openorca
      ```
      You can pick any model you want from this
      location [https://localai.io/docs/getting-started/run-other-models/](https://localai.io/docs/getting-started/run-other-models/)

### Usage

1. **Create a Virtual Environment (optional but recommended)**:
    - Open a terminal or command prompt and go to the cloned project directory
    - Run the following command to create a virtual environment named `env`:

        ```
        python -m venv env
        ```

    - Activate the virtual environment:
        - On Windows:
            ```
            .\env\Scripts\activate
            ```
        - On macOS and Linux:
            ```
            source env/bin/activate
            ```

2. **Install Dependencies from requirements.txt**:
    - Run the following command to install the dependencies:

        ```
        pip install -r requirements.txt
        ```

3. **Run the Flask Application**:
    - Run the following command to start the flask service:

        ```
        python main.py
        ```

   This command will start the Flask server, and you'll see output similar to:
    ```
     * Running on http://127.0.0.1:8008/ (Press CTRL+C to quit)
    ```

   The application should now be running locally.
   You can also change the running port by modifying the port variable `SERVICE_PORT` in .env file.

### Running the API

If you already have a .mp3 file or .wav file with you can pass the path to the API

```commandline
curl --location 'http://127.0.0.1:8008/summarize_conversation' --header 'Content-Type: application/json' --data '{ "audio_file_path" : "/home/leopard/demo.mp3" }'
```

*Note*: If you are running this service on CPU it may take a while for the API to complete the processing. Take a break.

## Acknowledgements

Open source tools used in this proof of concept.

* `pyannote.audio` is an open-source toolkit written in Python for speaker diarization.
  https://pypi.org/project/pyannote.audio/

* `pydub` Manipulate audio with a simple and easy high level interface.
  https://pypi.org/project/pydub/

* https://huggingface.co/pyannote/speaker-diarization

* `localai.io` is a free, Open Source OpenAI alternative. https://localai.io/