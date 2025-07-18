# trenddit

## Reddit Stock Sentiment Analyzer

Ever wondered if Reddit can predict stock market trends? This project dives into the world of meme stocks, market hype, and real sentiment—analyzing what Redditors are saying and how it aligns with stock price movements. Built with natural language processing and a touch of financial curiosity, this tool aims to uncover patterns between social chatter and market behavior.

---

### Features

> **Real-Time Reddit Scraping** – Pulls the latest posts and comments about specific tickers from Reddit.

> **Sentiment Analysis** – Uses NLP to evaluate whether the crowd is bullish, bearish, or just plain confused.

> **Stock Price Correlation** – Matches sentiment trends with actual market movements.

> **Trend Insights** – Offers basic predictive insights to spark your trading ideas.

---

### ⚙️ Setup

1. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Reddit API Setup**  
   Create a `.env` file in your root directory and add your Reddit API credentials:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   ```

3. **Run the Analyzer**  
   ```bash
   python stock_sentiment.py
   ```
---

### Requirements

```bash
praw==7.7.1
pandas==2.1.0
numpy==1.24.3
scikit-learn==1.3.0
nltk==3.8.1
yfinance==0.2.28
python-dotenv==1.0.0
flask==2.3.3
werkzeug==2.3.7
matplotlib==3.7.1
seaborn==0.12.2 
```

---

### Caution!

> This project is designed for **educational purposes** and experimenting with sentiment analysis. It is **not** financial advice. Always do your own research before making any investment decisions.

---

### Future Ideas

- Integrate with Twitter sentiment for broader social media trends  
> Any ideas from your end are most welcome!
