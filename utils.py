import asyncio
import nltk
import matplotlib.pyplot as plt
from scrapes import get_valid_news_urls, extract_article_content
from sentiV_v2 import analyze_sentiment
from newspaper import Article, Config
from deep_translator import GoogleTranslator  # Replaced googletrans with deep-translator

# Helper: Chunk text into smaller parts based on a fixed word count
def chunk_text_by_words(text, chunk_size=100):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def process_articles(company_name):
    """Extract articles with metadata from news URLs and only keep those relevant to the company."""
    urls = get_valid_news_urls(company_name)
    articles = []
    # Set up a custom config with a browser user-agent to help avoid 403 errors
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36')
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    for url in urls:
        try:
            art = Article(url, config=config)
            art.download()
            art.parse()
            content = art.text.strip() if art.text.strip() else extract_article_content(url)
            # Filter out articles that do not mention the company (case-insensitive)
            if not content or company_name.lower() not in content.lower():
                continue
            article_data = {
                "title": art.title if art.title else "No Title",
                "url": url,
                "date": str(art.publish_date) if art.publish_date else "N/A",
                "content": content
            }
            sentiment, score = analyze_sentiment(content)
            article_data["sentiment"] = sentiment
            article_data["score"] = score
            articles.append(article_data)
        except Exception as e:
            print(f"Error processing article {url}: {e}")
    return articles

def generate_combined_summary(articles):
    """Generate a combined summary from articles.
       First attempts to use a transformers pipeline; if it fails, falls back to Sumy."""
    combined_text = " ".join([article["content"] for article in articles])
    if not combined_text.strip():
        return ""
    # Try using transformers summarizer
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Transformers summarization failed: {e}")
        # Fallback using Sumy extraction-based summarization
        try:
            from sumy.parsers.plaintext import PlaintextParser
            from sumy.nlp.tokenizers import Tokenizer
            from sumy.summarizers.lex_rank import LexRankSummarizer
            parser = PlaintextParser.from_string(combined_text, Tokenizer("english"))
            summarizer_sumy = LexRankSummarizer()
            summary_sentences = summarizer_sumy(parser.document, sentences_count=5)
            summarized_text = " ".join(str(sentence) for sentence in summary_sentences)
            return summarized_text if summarized_text else combined_text[:500]
        except Exception as e2:
            print(f"Sumy summarization failed: {e2}")
            return combined_text[:500]

def translate_to_hindi(text):
    """Translate English text to Hindi using deep-translator for better quality."""
    try:
        translator = GoogleTranslator(source='auto', target='hi')
        return translator.translate(text)
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def comparative_analysis(articles):
    """Perform comparative sentiment analysis across articles and generate a bar chart."""
    pos, neg, neu = 0, 0, 0
    for article in articles:
        sentiment = article.get("sentiment", "Neutral")
        if sentiment == "Positive":
            pos += 1
        elif sentiment == "Negative":
            neg += 1
        else:
            neu += 1

    # Create a bar chart using matplotlib
    labels = ['Positive', 'Negative', 'Neutral']
    counts = [pos, neg, neu]
    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, counts, color=['green', 'red', 'gray'])
    plt.title("Comparative Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, str(count), ha='center', va='bottom')
    image_path = "sentiment_analysis.png"
    plt.savefig(image_path)
    plt.close()
    return {"Positive": pos, "Negative": neg, "Neutral": neu, "graph": image_path}

def generate_tts_audio(text, output_file="news_summary.mp3"):
    """Generate TTS audio file from text using Edge TTS (via tts_hindi_edgetts.py)."""
    try:
        from tts_hindi_edgetts import text_to_speech_hindi
        return asyncio.run(text_to_speech_hindi(text, output_file))
    except Exception as e:
        print(f"TTS generation failed: {e}")
        return None

def process_news(company_name):
    """
    Process news by:
      • Extracting articles and metadata (only those relevant to the company)
      • Generating a combined summary of article contents
      • Translating the summary to Hindi
      • Generating a Hindi TTS audio file
      • Performing comparative sentiment analysis with visual output
    """
    articles = process_articles(company_name)
    summary = generate_combined_summary(articles)
    hindi_summary = translate_to_hindi(summary)
    tts_audio = generate_tts_audio(hindi_summary)
    sentiment_distribution = comparative_analysis(articles)
    result = {
        "company": company_name,
        "articles": articles,
        "comparative_sentiment": sentiment_distribution,
        "final_summary": summary,
        "hindi_summary": hindi_summary,
        "tts_audio": tts_audio  # file path for the generated audio
    }
    return result

if __name__ == "__main__":
    company = input("Enter company name: ")
    import json
    data = process_news(company)
    print(json.dumps(data, indent=4, ensure_ascii=False))
