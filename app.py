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

DEFAULT_TEXT = """This document reflects the strategy we’ve refined over the past two years, including feedback from many people internal and external to OpenAI. The timeline to AGI remains uncertain, but our Charter will guide us in acting in the best interests of humanity throughout its development.

OpenAI’s mission is to ensure that artificial general intelligence (AGI)—by which we mean highly autonomous systems that outperform humans at most economically valuable work—benefits all of humanity. We will attempt to directly build safe and beneficial AGI, but will also consider our mission fulfilled if our work aids others to achieve this outcome. To that end, we commit to the following principles:
Broadly distributed benefits

We commit to use any influence we obtain over AGI’s deployment to ensure it is used for the benefit of all, and to avoid enabling uses of AI or AGI that harm humanity or unduly concentrate power.

Our primary fiduciary duty is to humanity. We anticipate needing to marshal substantial resources to fulfill our mission, but will always diligently act to minimize conflicts of interest among our employees and stakeholders that could compromise broad benefit.
Long-term safety

We are committed to doing the research required to make AGI safe, and to driving the broad adoption of such research across the AI community.

We are concerned about late-stage AGI development becoming a competitive race without time for adequate safety precautions. Therefore, if a value-aligned, safety-conscious project comes close to building AGI before we do, we commit to stop competing with and start assisting this project. We will work out specifics in case-by-case agreements, but a typical triggering condition might be “a better-than-even chance of success in the next two years.”
Technical leadership

To be effective at addressing AGI’s impact on society, OpenAI must be on the cutting edge of AI capabilities—policy and safety advocacy alone would be insufficient.

We believe that AI will have broad societal impact before AGI, and we’ll strive to lead in those areas that are directly aligned with our mission and expertise.
Cooperative orientation

We will actively cooperate with other research and policy institutions; we seek to create a global community working together to address AGI’s global challenges.

We are committed to providing public goods that help society navigate the path to AGI. Today this includes publishing most of our AI research, but we expect that safety and security concerns will reduce our traditional publishing in the future, while increasing the importance of sharing safety, policy, and standards research.
"""

st.set_page_config(page_title="AI Text-to-Speech",
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

text = st.text_area("Your text", value = DEFAULT_TEXT, max_chars=4096, height=500)
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
