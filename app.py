import os
import time
import requests
import streamlit as st
import uvicorn  # Add this
from fastapi import FastAPI
from utils import process_news

import spacy
try:
    spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")

# FastAPI app setup
api = FastAPI(title="News Summarization & TTS API")

@api.get("/")
def read_root():
    return {"message": "Welcome to the News Summarization & TTS API"}

@api.get("/news/{company_name}")
def get_news(company_name: str):
    return process_news(company_name)

# Streamlit app setup
API_URL = "http://127.0.0.1:8000"  # Use localhost instead of 0.0.0.0

st.title("News Summarization and Hindi TTS Application")
company = st.text_input("Enter Company Name", "")

if st.button("Fetch News"):
    if company.strip() == "":
        st.warning("Please enter a valid company name.")
    else:
        with st.spinner("Fetching and processing news..."):
            time.sleep(2)  # Give FastAPI some time to start
            try:
                response = requests.get(f"{API_URL}/news/{company}")
                if response.status_code == 200:
                    data = response.json()
                    st.header(f"News for {data['company']}")

                    for article in data["articles"]:
                        st.subheader(article.get("title", "No Title"))
                        st.markdown(f"**URL:** [Read More]({article.get('url', '#')})")
                        st.markdown(f"**Date:** {article.get('date', 'N/A')}")
                        st.markdown(f"**Sentiment:** {article.get('sentiment', 'Neutral')} (Score: {article.get('score', 0):.2f})")
                        st.markdown(f"**Excerpt:** {article.get('content','')[:300]}...")
                        st.markdown("---")

                    st.subheader("Comparative Sentiment Analysis")
                    comp_sent = data.get("comparative_sentiment", {})
                    st.write({k: comp_sent[k] for k in ["Positive", "Negative", "Neutral"]})

                    if "graph" in comp_sent and os.path.exists(comp_sent["graph"]):
                        st.image(comp_sent["graph"], caption="Sentiment Analysis Graph")

                    st.subheader("Final Combined Summary")
                    st.write(data.get("final_summary", "No summary available."))

                    st.subheader("Hindi Summary")
                    st.write(data.get("hindi_summary", ""))

                    st.subheader("Hindi Summary Audio")
                    audio_path = data.get("tts_audio", None)
                    if audio_path and os.path.exists(audio_path):
                        with open(audio_path, "rb") as audio_file:
                            st.audio(audio_file.read(), format='audio/mp3')
                    else:
                        st.error("Audio file not found or TTS generation failed.")
                else:
                    st.error("Failed to fetch news from the API. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("API is not running yet. Please wait a moment and try again.")

# 🛠️ **Start FastAPI Server**
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: uvicorn.run(api, host="127.0.0.1", port=8000), daemon=True).start()
