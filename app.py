import os
import streamlit as st
from video_transcription import transcribe_audio, transcribe_video, download_audio_from_link

# Set your OpenAI API Key as an environment variable
os.environ['OPENAI_API_KEY'] = 'your_api_key_here'

st.title("Audio Transcription using OpenAI Whisper API")

option = st.radio("Choose an option:", ('Upload a video file', 'Enter a YouTube or podcast link'))

if option == 'Upload a video file':
    uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_video is not None:
        with st.spinner("Transcribing video..."):
            transcript = transcribe_video(uploaded_video)

        st.subheader("Transcription")
        st.write(transcript)

elif option == 'Enter a YouTube or podcast link':
    video_link = st.text_input("Enter a YouTube or podcast link")

    if video_link:
        with st.spinner("Downloading audio..."):
            audio_file = "downloaded_audio.wav"
            download_audio_from_link(video_link, audio_file)

        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(audio_file)

        st.subheader("Transcription")
        st.write(transcript)

save_button = st.button("Save Transcription to File")
if save_button and transcript:
    transcript_file = "transcription.txt"
    with open(transcript_file, 'w') as f:
        f.write(transcript)
    st.success(f"Transcription saved to {transcript_file}")
