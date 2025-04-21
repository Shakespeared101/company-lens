---
title: "Company Lens"
emoji: "📰"
colorFrom: "blue"
colorTo: "green"
sdk: "streamlit"
app_file: "app.py"
pinned: false
---
# Company Lens

## Project Overview

This project is a web-based application that extracts news articles from multiple sources for a given company, summarizes the articles using advanced NLP techniques (with both Transformer-based and fallback methods), performs sentiment analysis with visual graphs, translates the generated summary to Hindi, and finally converts the Hindi summary into an audio file via text-to-speech (TTS). The application is built using FastAPI for the backend and Streamlit for the frontend, ensuring a smooth and interactive user experience.

## Features

- **News Extraction:**  
  Extracts news articles from multiple sources using web scraping techniques.

- **Summarization:**  
  Generates a combined summary using a Transformer-based summarizer (with fallback to Sumy if needed).

- **Sentiment Analysis:**  
  Analyzes the sentiment of the news content and visualizes the comparative sentiment (Positive, Negative, Neutral) as a bar graph using matplotlib.

- **Translation:**  
  Translates the summary from English to Hindi using googletrans for improved quality.

- **Text-to-Speech (TTS):**  
  Converts the Hindi summary into an audio file using Edge TTS.

## Setup Instructions

### Dependencies

Install all required packages using the command below:

```bash
pip install fastapi uvicorn streamlit transformers newspaper3k beautifulsoup4 edge-tts selenium webdriver-manager spacy nltk sumy sacremoses requests googletrans==4.0.0-rc1 matplotlib
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

### Running the FastAPI Backend

In your project directory, run:

```bash
uvicorn api:app --reload
```

This will start the backend server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Running the Streamlit Frontend

In another terminal (or a new tab), run:

```bash
streamlit run streamlit_app.py
```

This will launch the web interface where you can input a company name and interact with the application.

## Project Structure

- **`api.py`**  
  Contains the FastAPI application which exposes endpoints for processing news, generating summaries, performing sentiment analysis, translating summaries to Hindi, and creating TTS audio.

- **`utils.py`**  
  Houses utility functions for:
  - Extracting articles from news URLs.
  - Generating combined summaries using Transformer models with Sumy as a fallback.
  - Translating text to Hindi using googletrans.
  - Performing comparative sentiment analysis and generating a matplotlib bar chart.
  - Generating TTS audio from the Hindi summary.

- **`streamlit_app.py`**  
  Provides a simple and interactive web-based interface using Streamlit. Users can input a company name, view extracted news and summaries, see the sentiment analysis graph, and play the generated TTS audio.

- **`scrapes.py`**  
  Contains functions for scraping valid news URLs and extracting article content from web pages.

- **`sentiV_v2.py`**  
  Implements sentiment analysis on the article content using both NLTK’s VADER and Transformer-based methods.

- **`tts_hindi_edgetts.py`**  
  Utilizes Edge TTS to convert text to speech and saves the output as an audio file.

- **`.gitignore`**  
  Ensures that large or unnecessary files (like the virtual environment folder `venv/`) are not tracked by Git.

## Deployment Details

The application can be deployed on platforms like [Hugging Face Spaces](https://huggingface.co/spaces), Heroku, or Render. For example, if deployed on Hugging Face Spaces:

- The repository is linked to a new Space.
- The Streamlit interface is used as the main application.
- The deployment link (e.g., `https://huggingface.co/spaces/your-username/news-summarisation`) will be provided in the repository README for access.

## Usage Instructions

1. **Launch the Application:**  
   Run the FastAPI backend and Streamlit frontend as described above.

2. **Input a Company Name:**  
   On the Streamlit interface, enter the name of a company (e.g., "Tesla", "Netflix") and click the "Fetch News" button.

3. **View Results:**  
   - **News Articles:**  
     See a list of extracted news articles along with their metadata (title, URL, date, sentiment, excerpt).
   - **Sentiment Analysis:**  
     View the comparative sentiment counts and a bar chart visualizing the distribution of positive, negative, and neutral articles.
   - **Summaries:**  
     Read the combined summary of the news and the translated Hindi summary.
   - **Audio:**  
     Play the TTS-generated audio of the Hindi summary.

## Limitations & Future Improvements

### Limitations:

- Reliance on web scraping can sometimes result in incomplete article extraction due to website restrictions.
- The summarization and translation quality might vary based on input length and complexity.
- TTS accuracy depends on the Edge TTS service and may not always be perfect.

### Future Improvements:

- Integrate more robust error handling and fallback mechanisms.
- Enhance the UI for better user experience.
- Expand the number of news sources and improve the filtering of relevant content.
- Implement caching to reduce API call latency.
- Explore additional TTS options for higher quality audio output.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to contribute to this project.
