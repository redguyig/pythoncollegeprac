
import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Language Translator", layout='centered')
st.title("Voice-Based Language Translator")

LANGUAGES = {
    'en': 'English', 'fr': 'French', 'es': 'Spanish',
    'hi': 'Hindi', 'de': 'German', 'it': 'Italian',
    'zh-cn': 'Chinese (Simplified)', 'ja': 'Japanese',
    'ko': 'Korean', 'ar': 'Arabic', 'ru': 'Russian', 'pt': 'Portuguese',
}

lang_name = [name for name in LANGUAGES.values()]
lang_code = {v: k for k, v in LANGUAGES.items()}

# Language selection UI
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox(" Source Language", lang_name, index=lang_name.index("English"))
with col2:
    target_lang = st.selectbox(" Target Language", lang_name, index=lang_name.index("Hindi"))

spoken_text = ""

# Voice input handling
if st.button("Speak Now"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        spoken_text = recognizer.recognize_google(audio, language=lang_code[source_lang])
        st.success(f"You said: {spoken_text}")
    except Exception as e:
        st.error(f"Speech recognition error: {e}")

# Translation section
if spoken_text:
    try:
        translated_text= GoogleTranslator(source=lang_code[source_lang], target=lang_code[target_lang]).translate(spoken_text)
        st.success("Translated Text:")
        st.text_area(" Output", translated_text, height=120)
    except Exception as e:
        st.error(f"Translation failed: {e}")

if translated_text:
    if st.button(" Speak Output"):
        try:
            tts = gTTS(text=translated_text, lang=lang_code[target_lang])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_file = fp.name
            # Play audio file
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
