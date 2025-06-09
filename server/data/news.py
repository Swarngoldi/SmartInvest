import pandas as pd
import requests
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load the CSV file
csv_file = "Largecap.csv"  # Update with your CSV path
stocks_df = pd.read_csv(csv_file)

# Initialize a **financial-specific sentiment analysis model**
finbert_model = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
sentiment_analysis = pipeline(
    "sentiment-analysis",
    model=finbert_model,
    tokenizer=finbert_model
)

# Function to fetch news articles (with error handling)
def fetch_news(stock_name, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_name}&language=en&sortBy=publishedAt&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        news_data = response.json()
        return news_data.get('articles', [])
    except Exception as e:
        print(f"Error fetching news for {stock_name}: {e}")
        return []

# Function to analyze sentiment (with detailed debugging)
def analyze_sentiment(articles):
    if not articles:
        return "No News"  # Handle empty news case
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for article in articles[:5]:  # Analyze top 5 articles to avoid rate limits
        title = article.get('title', '')
        description = article.get('description', '')
        combined_text = f"{title}. {description}".strip()
        
        if not combined_text:
            continue
        
        try:
            # Get sentiment (financial model returns 'positive', 'negative', or 'neutral')
            sentiment_result = sentiment_analysis(combined_text, truncation=True, max_length=512)
            sentiment = sentiment_result[0]['label'].lower()
            
            # Debug print (comment out later)
            print(f"\nText: {combined_text[:100]}...\nSentiment: {sentiment}")
            
            if sentiment == 'positive':
                positive_count += 1
            elif sentiment == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            continue
    
    print(f"Results: Positive={positive_count}, Negative={negative_count}, Neutral={neutral_count}")
    
    # Determine overall sentiment (with threshold)
    total = positive_count + negative_count + neutral_count
    if total == 0:
        return "No News"
    
    positive_ratio = positive_count / total
    negative_ratio = negative_count / total
    
    if positive_ratio > 0.5:
        return "Positive"
    elif negative_ratio > 0.5:
        return "Negative"
    else:
        return "Neutral"

# API Key for NewsAPI (replace with your actual key)
api_key = 'bc6b7b73046b4c1397b4d153e027dcd4'  # This is a placeholder - use your own key

# Update News Sentiment in CSV
for index, row in stocks_df.iterrows():
    stock_name = row['Full Name']
    print(f"\nFetching news for: {stock_name}")
    articles = fetch_news(stock_name, api_key)
    sentiment = analyze_sentiment(articles)
    stocks_df.at[index, 'News Sentiment'] = sentiment
    print(f"Final Sentiment for {stock_name}: {sentiment}")

# Save the updated CSV
updated_csv_path = "Largecap.csv"
stocks_df.to_csv(updated_csv_path, index=False)
print(f"\nUpdated CSV saved as '{updated_csv_path}'")