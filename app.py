"""
app.py
"""
import streamlit as st
from openai import OpenAI

from utils import (
    append_to_sheet,
    moderation_check,
    text_to_speech,
    zero_shot_nsfw_classifier
)

st.set_page_config(page_title="Demo: Text-to-Speech",
                   page_icon="🎙")

st.title("OpenAI's Text-to-Speech 🎙")
with st.expander("About this app"):
    st.info("""
    This is a personal project, not affliated with OpenAI.
            
    **Is this really free?** I have some OpenAI API credits expiring on 1 March 2024. So... yes :)
    
    **Contact:** [X](https://www.x.com/gabchuayz) or [LinkedIn](https://www.linkedin.com/in/gabriel-chua)
    """)
    
if "audio" not in st.session_state:
    st.session_state["audio"] = None

text = st.text_area("Your text", max_chars=4096)
voice = st.radio("Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], horizontal = True, help="Previews can be found [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options)")

if st.button("Generate Audio"):

    if len(text) == 0:
        st.warning("Please enter a text.", icon="🚫")

    if (moderation_check(text)) or (zero_shot_nsfw_classifier(text) == 1):
        st.warning("This text has been flagged as NSFW. Please revise it.", icon="🚫")
        append_to_sheet(text, voice, False)
        st.stop()
    
    with st.spinner("Generating your audio - this can take up to 30 seconds..."):
        st.session_state["audio"] = text_to_speech(text, voice)
        append_to_sheet(text, voice, True)

        audio_file = open("audio.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.download_button(label="Download audio",
                             data=audio_bytes,
                             file_name="audio.mp3",
                             mime="audio/mp3")
