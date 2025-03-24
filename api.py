from fastapi import FastAPI
from utils import process_news
import os

app = FastAPI(title="News Summarization & TTS API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summarization & TTS API"}

@app.get("/news/{company_name}")
def get_news(company_name: str):
    """
    Fetch processed news for a given company.
    Returns:
      • A list of articles with title, URL, date, content, sentiment, and score.
      • A combined summary of all articles.
      • A Hindi translated summary.
      • The TTS audio file path.
      • Comparative sentiment analysis including a visual graph.
    """
    return process_news(company_name)

# Hugging Face automatically runs this service
if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))  # Hugging Face assigns a dynamic port
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
