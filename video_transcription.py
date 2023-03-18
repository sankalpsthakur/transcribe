import os
import json
import requests
from pydub import AudioSegment
from moviepy.editor import *

def extract_audio_from_video(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio

    temp_audio_file = "temp_audio.wav"
    audio.write_audiofile(temp_audio_file, codec="pcm_s16le")

    sound = AudioSegment.from_wav(temp_audio_file)
    sound = sound.set_frame_rate(16000)  # Reduce the sample rate
    sound.export(audio_file, format="wav")

    os.remove(temp_audio_file)

def download_audio_from_link(link, output_file):
    """
    Download audio from a YouTube or podcast link and save it as a WAV file.
    """
    # Check if the link is a YouTube video
    if "youtube.com/watch" in link or "youtu.be/" in link:
        # Use youtube-dl to download the audio from the YouTube video as a WAV file
        os.system(f"youtube-dl -f 'bestaudio[ext!=webm]' -x --audio-format wav --audio-quality 0 --output {output_file} {link}")
        
        # Load the downloaded WAV file using PyDub and set the frame rate to 16KHz
        sound = AudioSegment.from_wav(output_file)
        sound = sound.set_frame_rate(16000)
        sound.export(output_file, format="wav")
    
    # Check if the link is a podcast
    elif link.endswith(".mp3"):
        # Download the MP3 file from the podcast link
        response = requests.get(link)
        
        # Write the content of the MP3 file to the output file as a WAV file
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        # Load the downloaded WAV file using PyDub and set the frame rate to 16KHz
        sound = AudioSegment.from_mp3(output_file)
        sound = sound.set_frame_rate(16000)
        sound.export(output_file, format="wav")
    
    # If the link is not a YouTube video or a podcast, raise an exception
    else:
        raise Exception("Invalid link. Please enter a YouTube or podcast link.")

def transcribe_audio(audio_file):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    }
    
    # Include the model parameter in the request data as a form field
    data = {
        "model": "whisper-1"
    }

    with open(audio_file, "rb") as audio:
        response = requests.post(url, headers=headers, data=data, files={"file": audio})

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.text)
        raise Exception(f"Whisper API returned an error: {response.text}")

def transcribe_video(video_file):
    audio_file = "extracted_audio.wav"
    extract_audio_from_video(video_file, audio_file)
    transcription_result = transcribe_audio(audio_file)
    transcription = transcription_result['text']
    return transcription
