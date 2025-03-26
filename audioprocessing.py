import streamlit as st
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioDataStream, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioConfig
import requests
import json
import os

# Azure multi-service credentials
azure_key = os.environ["AZURE_AI_KEY"]
service_region = os.environ["AZURE_AI_REGION"]
azure_endpoint = os.environ["AZURE_AI_ENDPOINT"]

# Streamlit app
st.title("Audio Translation App")
st.write("Upload an audio file to transcribe, translate to French, and convert back to audio.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded file
    with open("uploaded_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Transcribe audio using Azure Speech Service
    speech_config = SpeechConfig(subscription=azure_key, endpoint=azure_endpoint)
    audio_config = AudioConfig(filename="uploaded_audio.wav")
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    st.write("Transcribing audio...")
    result = recognizer.recognize_once()
    
    if result.reason == result.reason.RecognizedSpeech:
        st.write("Transcription: ", result.text)
        transcription = result.text
        
        # Translate text using Azure Translator Text API
        st.write("Translating text...")
        headers = {
            "Ocp-Apim-Subscription-Key": azure_key,
            "Ocp-Apim-Subscription-Region": service_region,  # Replace with your Azure region
            "Content-Type": "application/json"
        }
        body = [{
            "text": transcription
        }]
        translate_url = f"{azure_endpoint}/translator/text/v3.0/translate?to=fr"
        
        response = requests.post(translate_url, headers=headers, json=body)
        if response.status_code == 200:
            translation_result = response.json()
            translated_text = translation_result[0]["translations"][0]["text"]
            st.write("Translation: ", translated_text)
            
            # Convert translated text to audio using Azure Text-to-Speech
            audio_config = AudioConfig(filename="translated_audio.wav")  # Use AudioConfig for output
            synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            
            st.write("Converting translated text to audio...")
            synthesizer.speak_text_async(translated_text).get()
            
            # Provide download link for the translated audio file
            st.audio("translated_audio.wav", format="audio/wav")
            # Provide a button to listen to the translated audio
            if st.button("Play Translated Audio"):
                st.audio("translated_audio.wav", format="audio/wav")
                st.success("Playing translated audio!")
            st.success("Translation and conversion completed successfully!")
        else:
            st.error("Translation failed. Error: " + response.text)
    else:
        st.error("Transcription failed.")