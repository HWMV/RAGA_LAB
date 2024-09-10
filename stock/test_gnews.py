from gnews import GNews
from datetime import datetime


def stock_news(ticker):
    """
    Get URLs of news articles related to a stock from 2023-12-01 to 2024-01-01.
    The input to this tool should be a ticker, for example AAPL, NET
    """
    start_date = datetime(2023, 12, 1)
    end_date = datetime(2024, 1, 1)
        
    google_news = GNews(language='en', country='US', start_date=start_date, end_date=end_date)
    news = google_news.get_news(f"{ticker} stock")
    return [article['url'] for article in news]

ticker = "NVDA"
gnews_test = stock_news(ticker)
print(gnews_test)