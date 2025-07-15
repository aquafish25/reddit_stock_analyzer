import os
import nltk
import praw
import numpy as np
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
load_dotenv()

class StockSentimentAnalyzer:
    def __init__(self):
        """
        Initializes the StockSentimentAnalyzer class by setting up the Reddit API client 
        and the Sentiment Intensity Analyzer.

        The Reddit API client is configured using environment variables for authentication, 
        and the Sentiment Intensity Analyzer is initialized to perform sentiment analysis 
        on text data.
        """

        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        self.sia = SentimentIntensityAnalyzer()

    def get_reddit_posts(self, stock_symbol, limit=100):
        """
        Retrieves Reddit posts related to a specific stock symbol from the 'stocks',
        'investing', and 'wallstreetbets' subreddits.

        Args:
            stock_symbol (str): The stock symbol to search for in Reddit posts.
            limit (int, optional): The maximum number of posts to retrieve. Default is 100.

        Returns:
            pandas.DataFrame: A DataFrame containing the posts with their title, text,
            score, and creation date in UTC.
        """
        posts = []
        for post in self.reddit.subreddit('stocks+investing+wallstreetbets').search(
            f'{stock_symbol} stock', limit=limit
        ):
            posts.append({
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'created_utc': datetime.fromtimestamp(post.created_utc)
            })
        return pd.DataFrame(posts)

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of a given text using the SentimentIntensityAnalyzer.

        Args:
            text (str): The text to analyze the sentiment of.

        Returns:
            float: The sentiment score of the text, ranging from -1 (very negative) to
            1 (very positive).
        """
        return self.sia.polarity_scores(text)['compound']

    def get_stock_data(self, stock_symbol, days=30):
        """
        Retrieves historical stock data for a specified symbol over a given number of days.

        Args:
            stock_symbol (str): The stock symbol to fetch historical data for.
            days (int, optional): The number of days of historical data to retrieve, counting back from today. Default is 30.

        Returns:
            pandas.DataFrame: A DataFrame containing the historical stock data, including open, high, low, close prices, and volume.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        stock = yf.Ticker(stock_symbol)
        return stock.history(start=start_date, end=end_date)

    def predict_trend(self, stock_symbol):
        """
        Predicts the stock trend based on Reddit sentiment analysis for a given stock symbol.

        This method retrieves Reddit posts related to the specified stock symbol, analyzes
        the sentiment of the posts, and calculates the average sentiment score. Based on the
        sentiment analysis, it predicts whether the trend is bullish, bearish, or neutral.

        Args:
            stock_symbol (str): The stock symbol to predict the trend for.

        Returns:
            str: A string indicating the predicted trend: "Bullish", "Bearish", or "Neutral",
            along with a brief explanation of the detected sentiment.
        """
        posts_df = self.get_reddit_posts(stock_symbol)
        posts_df['sentiment'] = posts_df['text'].apply(self.analyze_sentiment)
        avg_sentiment = posts_df['sentiment'].mean()
        stock_data = self.get_stock_data(stock_symbol)
        if avg_sentiment > 0.2:
            return "Bullish (Detected - Positive sentiment)"
        elif avg_sentiment < -0.2:
            return "Bearish (Detected - Negative sentiment)"
        else:
            return "Neutral (Detected - Mixed sentiment)"

def main():
    """
    Main execution function.

    Initializes the StockSentimentAnalyzer and prompts the user to enter a stock symbol.
    Then, it uses the analyzer to predict the stock trend and prints the prediction.
    Additionally, it shows some sample Reddit posts about the stock along with their
    sentiment analysis.

    If an error occurs during the execution, it will be caught and printed to the console.
    """

    analyzer = StockSentimentAnalyzer()
    stock_symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    try:
        prediction = analyzer.predict_trend(stock_symbol)
        print(f"\nAnalysis for {stock_symbol}:")
        print(prediction)
        
        posts = analyzer.get_reddit_posts(stock_symbol, limit=5)
        print("\nRecent Reddit posts about this stock:")
        for _, post in posts.iterrows():
            print(f"\nTitle: {post['title']}")
            print(f"Sentiment: {analyzer.analyze_sentiment(post['text']):.2f}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 