import torch
from dotenv import dotenv_values
from pyannote.audio import Pipeline
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
# Diarization Pipeline START #
config = dotenv_values(".env")
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                use_auth_token=config.get("HUGGINGFACE_ACCESS_TOKEN"))
# send pipeline to GPU (when available)
diarization_pipeline.to(torch.device(device))
# Diarization Pipeline END #

# Audio Transcription Pipline START #

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True,
                                                  use_safetensors=True)
model.to(device)
processor = AutoProcessor.from_pretrained(model_id)
audio_transcription_pipeline = pipeline("automatic-speech-recognition", model=model_id, tokenizer=processor.tokenizer,
                                        feature_extractor=processor.feature_extractor, max_new_tokens=128,
                                        chunk_length_s=30, batch_size=16, return_timestamps=True,
                                        torch_dtype=torch_dtype, device=device, )

# Audio Transcription Pipline END #
