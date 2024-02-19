"""
utils.py
"""
import json
from datetime import datetime
from pathlib import Path

import gspread
import streamlit as st
from google.oauth2 import service_account
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def append_to_sheet(text, voice, generated):
    """
    Add to GSheet
    """
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(st.secrets["GCP_SERVICE_ACCOUNT"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url(st.secrets["PRIVATE_GSHEETS_URL"])
    worksheet = sh.get_worksheet(0) # Assuming you want to write to the first sheet
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([current_time, text, voice, generated])

def moderation_check(text):
    """Check if the given text is safe for work using openai's moderation endpoint."""
    response = client.moderations.create(input=text)
    return response.results[0].flagged

def zero_shot_nsfw_classifier(text):
    """Check if the given text is safe for work using gpt4 zero-shot classifer."""
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "system", "content": "Is the given text NSFW? If yes, return `1`, else return `0`"},
                  {"role": "user", "content": text}],
        max_tokens=1,
        temperature=0,
        seed=0,
        logit_bias={"15": 100,
                    "16": 100}
    )

    return int(response.choices[0].message.content)

def text_to_speech(text, voice):
    speech_file_path = Path("audio.mp3")
    response = client.audio.speech.create(
      model="tts-1-hd",
      voice=voice,
      input=text
    )
    response.stream_to_file(speech_file_path)
