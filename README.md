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
Sample Output
```commandline
{
    "summary": "One-meal-a-day (OMAD) dieting is recommended over multiple small meals per day because it activates stress response pathways that promote longevity and disease resistance, similar to the body's response to periods of hunger. This is because, over millions of years, our bodies have evolved to respond to adversity such as food scarcity.\n\nFasting triggers the production of hormones that promote resilience and combat aging and diseases. Conversely, constantly eating signals to the body that resources are abundant, reducing the need for adaptability and resilience.\n\nThe speaker advocates for lengthening the window of not eating, suggesting that by skipping breakfast and waiting until around 11am for the first meal, the body can benefit from the stress response associated with fasting.\n\nThe speaker's personal experience of not eating before comedy shows and workouts supports the idea that a fasted state can enhance performance and reduce distractions.\n\nHowever, the speaker acknowledges that intense workouts can require post-exercise nutrition to support muscle recovery. In such cases, they recommend a light meal of meat and fruit as opposed to heavy or sugary foods.\n\nWhile the speaker advocates for fasting as a means to improve health and longevity, they also highlight that there are safe and effective supplements, such as NMN (nicotinamide mononucleotide), which can mimic the benefits of fasting and potentially enhance exercise performance, boost energy levels, and slow the aging process.\n\nThe speaker emphasizes that NMN is currently undergoing clinical trials and expresses their hope that it will soon be available to the public, depending on the regulatory approval process.",
    "transcript": "SPEAKER_01: Oh\nSPEAKER_00: The Joe Rogan experience. And what is going on with eating? So if you have one meal and say this meal comprises 2,000 calories or whatever, and you have this meal at 6 p.m. and you fast for 24 hours until you eat again at 6 p.m. If you have this one meal a day, why is it better to do that than to have, say, smaller meals of like 500 calories multiple times per day, little snacks.\nSPEAKER_01: Well, because going back six million years back, you know, we're in the trees and then in the savannah, our bodies were designed, well, or evolved to respond to adversity. And we've removed that from our lives because it feels good. But we need adversity to be resilient and to fight disease. So what I'm saying is that period of hunger, and it's not even hunger these days. I don't even feel it. I feel great if I don't eat. And it takes a few weeks. So anyone wants to start, give it some time, give it a couple of weeks. But what's happening in the body is you're turning on these adversity hormesis response genes. We call them longevity genes. And they make the body fight aging and diseases. And so by eating through the day, the traditional, oh, you got to have breakfast, best meal of the day, blah, blah, blah. First of all, it's not true that you need to be full or fed to think clearly. It's very clear that people who are fasting have as good, if not better, mental acuity. Okay, that's one. So I think that that needs to be thrown out the window. Kids are different. We're not talking about kids. We're talking about adults. And we're not talking about malnutrition or starvation too, let's be clear. But we are talking about lengthening that window of not eating. So if you always are satiated, fed, your body says, hey, I've just killed a mammoth. No problem. Don't need to worry about survival. I'm just going to go forth and multiply and screw my long-term survival. So this is all about long-term survival by making the body freak out that there's tough times. And that's running away, like running away from a cat, like the Savannah, and being hungry. There's molecular reasons that all this works, but trust me that the data is very clear that this is the way to go if you want to be healthy in your 80s and 90s.\nSPEAKER_00: So this is all about long-term survival by making the body freak out that there's tough times. And that's running away, like running away from a cat, like the savannah, and being hungry. You know, there's molecular reasons that all this works. But, you know, trust me, the data is very clear that this is the way to go if you want to be healthy in your 80s and 90s. Well, it actually does make sense when you put it in that way that your body, when you're fed, relaxes. And so if you're just doing that all day long, and I know for a fact that when I am not fed and I go and do things, whether it's perform, one of the things that I've been doing is I don't eat before shows. Like I take many, many hours before a comedy show. And I used to just like eat whenever. I just eat. And then I would do shows and I would have a meal like an hour before the show. And I'm really trying to wake up. I'm really trying to come on, come on, come on. But I've now recognized. Actually, I saw a video where Cat Williams was talking about this. Do you know who Cat Williams is? Hilarious comedian? I do know. Well, you're slipping if you don't. He's hilarious. When he was doing this interview and he was saying, what's your process before a show? And one of the things is I don't eat. I make sure I don't eat. And I was like, that's wise. That's really smart. And I'm like, I needed to hear that even though I kind of knew it, but I'd never written it down. I'd never like associated it absolutely. But now I have. Like now I do not eat before shows. I won't do it unless I know I have three hours. So what's your average day look like? It depends entirely on whether or not I'm doing podcasts. If I'm doing podcasts, generally I'm up early. I get my workouts in. I usually have something to eat after the workout. So I'm talking about like I eat around 11, 11 a.m. That's my first meal of the day. And then I go and do my stuff. And I generally feel like my workouts are so strenuous that I need some sort of nutrition afterwards, some sort of fruit to pump the muscles back up and give them some sugar and some protein. So usually I'm eating meat and maybe like an apple or something like that. That's like a normal meal for me. And then I don't eat again until nighttime. Great. And you're not snacking? No. Eh, maybe. Sometimes after a podcast I'll have like, we have these On It Warrior bars that are just buffalo meat and some cranberries and stuff. I like those. I'll eat one of those\nSPEAKER_01: Good. Well, at least you're going till 11. You got that sleep. Yeah. So you're probably not eating late anymore.\nSPEAKER_00: It's just the strenuous activity. My workouts are very hard. So after them, I feel like I need something. I don't like that feeling of a brutal workout and then being starving for four or five hours because then it becomes a distraction. So I listen to my body. But if I don't work out, I don't eat until dinner. Say a day like today, I didn't work out, I don't eat until dinner. Like say a day like today, I didn't work out today. So I woke up, hung out with the dog, had some coffee, sat out, you know, like just got went over some emails, did some shit, just a relaxed morning and then rolled into here. No food. I won't eat until we're going to dinner tonight. Great. Until then. Yeah. With Lex. Yes, that's going to be fun.\nSPEAKER_01: I won't eat until we're going to dinner tonight. Great. I won't eat until then. Yeah, with Lex. That'll be fun.\nSPEAKER_00: And John Donner.\nSPEAKER_01: Yeah, of course. Looking forward to meeting him. Yeah, so you're doing the right things, certainly better than most people. But what I'm trying to build or make are molecules that mimic fasting as well. So if you cannot fast like I do, then you can just take a pill. And what we've shown in mice, at least, is that if you give them this molecule that I'm taking, NMN, nicotinamide mononucleotide, which, as I mentioned, speeds up metabolisms, does a lot of stuff, those mice could run 50% further. These old mice, we gave it to them for three weeks,\nSPEAKER_00: looking forward to meeting him\nSPEAKER_01: put them back on a treadmill. And those that had the NMN in their water ran 50% for that. Better blood flow, better oxygenation, better energy. And that is literally exercise in a pill.\nSPEAKER_00: That's crazy.\nSPEAKER_01: So we're in late stage human clinical trials now.\nSPEAKER_00: When do you think it's going to be released to the public?\nSPEAKER_01: Well, it depends on what the FDA does and if it was mother fuckers. Oh, don't get me in trouble.\nSPEAKER_00: those motherfuckers\nSPEAKER_01: I love the FDA. I do too. Fair enough. They protect us. Yes. But yeah, we're going through the procedure that has been around since, as I mentioned, early 20th century. But it...\nSPEAKER_00: I do too. Fair enough. They protect us. Yes.\nSPEAKER_01: We've done hundreds of people now, certainly dozens, over the last few years. And we know at least that this molecule is apparently safe and raises the levels of the molecule we want to build up. The molecule is called NAD. Do you want me to talk a little bit about NAD? Yes, please. So NAD is what those mitochondria, little mechanite, little energy-producing things use.\nSPEAKER_00: Yes, please.\nSPEAKER_01: to make energy. So there are two molecules in the body that are really great. You need both for life. And without them, as I said, you're dead. ATP is the energy, and NAD makes that. And as we get older, the levels of NAD go down. Our body makes less and actually also degrades it more. So if you take my skin, or in the study that they took people's skin, when you're 50, you've got half the levels of this NAD than you did when you were 20, which is scary because this molecule is required for life. Without it, we're dead in 30 seconds. So what we're doing with our clinical trials is giving a precursor, a smaller version of this, that the body will turn into NAD and bring those levels back up from where they are when you're old to where you are when you're young. And we see at least in animals and hopefully in people that it revs up their metabolism and makes them fight aging and disease like we do when we're young. I mean, there's a reason we don't get a lot of heart disease when we're young or Alzheimer's because our bodies fight against disease as we get older. And especially if we sit around or smoke and don't exercise, our bodies just give up.\nSPEAKER_00: Catch new episodes of the Joe Rogan Experience for free only on Spotify. Watch back catalog JRE videos on Spotify, including clips. Easily, seamlessly switch between video and audio experience. On Spotify, you can listen to the JRE in the background while using other apps and can download episodes to save on data cost all for free. Spotify is absolutely free. You don't have to have a premium account to watch new JRE episodes. You just need to search for the JRE on your Spotify app. Go to Spotify now to get this full episode of the Joe Rogan Experience."
}
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