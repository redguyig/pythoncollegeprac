import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

LANGUAGES = {
    'en': 'English', 'fr': 'French', 'es': 'Spanish',
    'hi': 'Hindi', 'de': 'German', 'it': 'Italian',
    'zh-cn': 'Chinese (Simplified)', 'ja': 'Japanese',
    'ko': 'Korean', 'ar': 'Arabic', 'ru': 'Russian', 'pt': 'Portuguese',
}

st.title("Voice Translator ")

# Initialize session state variables
if 'spoken_text' not in st.session_state:
    st.session_state.spoken_text = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

def lang_code(lang_name):
    for code, name in LANGUAGES.items():
        if name == lang_name:
            return code
    return None


if st.button("Record Voice"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = recognizer.listen(source)
    try:
        st.session_state.spoken_text = recognizer.recognize_google(audio)
        st.success(f"You said: {st.session_state.spoken_text}")
        
        st.session_state.translated_text = ""
        st.session_state.audio_bytes = None
    except Exception as e:
        st.error(f"Speech recognition failed: {e}")


if st.session_state.spoken_text:
    st.write(f"**Recorded text:** {st.session_state.spoken_text}")

    st.session_state.source_lang = st.selectbox(
        "Select source language",
        options=list(LANGUAGES.values()),
        index=list(LANGUAGES.values()).index('English')
    )
    st.session_state.target_lang = st.selectbox(
        "Select target language",
        options=list(LANGUAGES.values()),
        index=list(LANGUAGES.values()).index('French')
    )

    
    if st.button("🌐 Translate"):
        try:
            st.session_state.translated_text = GoogleTranslator(
                source=lang_code(st.session_state.source_lang),
                target=lang_code(st.session_state.target_lang)
            ).translate(st.session_state.spoken_text)
            st.success(f"Translated text: {st.session_state.translated_text}")
            st.session_state.audio_bytes = None  # Reset audio when new translation occurs
        except Exception as e:
            st.error(f"Translation failed: {e}")


if st.session_state.translated_text:
    if st.button("Convert to Speech"):
        try:
            tts = gTTS(text=st.session_state.translated_text, lang=lang_code(st.session_state.target_lang))
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            st.session_state.audio_bytes = audio_fp
            st.success("Audio generated!")
        except Exception as e:
            st.error(f"TTS failed: {e}")


if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
