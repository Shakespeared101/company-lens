import os
import time
import requests
import streamlit as st

# 🔥 Change this to match your Hugging Face Space name
API_URL = "https://news-summarise-tts.hf.space"  # Replace with your actual Space URL

st.title("News Summarization and Hindi TTS Application")
company = st.text_input("Enter Company Name", "")

if st.button("Fetch News"):
    if company.strip() == "":
        st.warning("Please enter a valid company name.")
    else:
        with st.spinner("Fetching and processing news..."):
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
            except requests.exceptions.RequestException as e:
                st.error(f"API error: {e}")
