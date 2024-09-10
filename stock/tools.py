from crewai_tools import tool
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from gnews import GNews

class Tools:
    BASE_DATE = "2024-01-31"

    @tool("Stock price history")
    def stock_price(ticker):
        """
        Get stock price data for the last month before 2024-01-31 as CSV.
        The input should be a ticker (e.g., AAPL, NET, TSLA).
        """
        stock = yf.Ticker(ticker)
        end_date = datetime.strptime(Tools.BASE_DATE, "%Y-%m-%d")
        start_date = end_date - timedelta(days=30)
        return stock.history(start=start_date, end=end_date).to_csv()

    @tool("Stock news URLs")
    def stock_news(ticker):
        """
        Get URLs of news articles related to a stock from 2023-12-01 to 2024-01-31.
        The input to this tool should be a ticker, for example AAPL, NET
        """
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2024, 1, 31)

        # 나중에 max_result 늘려야 함    
        google_news = GNews(language='en', country='US', start_date=start_date, end_date=end_date, max_results=10)
        news = google_news.get_news(f"{ticker} stock")
        return [article['url'] for article in news]

    @tool("Company's income statement")
    def income_stmt(ticker):
        """
        Get the income statement of a stock as of 2024-01-31 as CSV.
        The input should be a ticker (e.g., AAPL, NET).
        """
        stock = yf.Ticker(ticker)
        financials = stock.financials
        filtered_financials = financials.loc[:, financials.columns <= Tools.BASE_DATE]
        return filtered_financials.to_csv()

    @tool("Balance sheet")
    def balance_sheet(ticker):
        """
        Get the balance sheet of a stock as of 2024-01-31 as CSV.
        The input should be a ticker (e.g., AAPL, NET).
        """
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet
        filtered_balance_sheet = balance_sheet.loc[:, balance_sheet.columns <= Tools.BASE_DATE]
        return filtered_balance_sheet.to_csv()

    @tool("Get insider transactions")
    def insider_transactions(ticker):
        """
        Get insider transactions of a stock for the last month before 2024-01-31 as CSV.
        The input should be a ticker (e.g., AAPL, NET).
        """
        try:
            stock = yf.Ticker(ticker)
            insider_transactions = stock.insider_transactions
            
            if insider_transactions.empty:
                return "No insider transactions data available for this stock."
            
            insider_transactions['Date'] = pd.to_datetime(insider_transactions['Date'])
            
            end_date = datetime.strptime(Tools.BASE_DATE, "%Y-%m-%d")
            start_date = end_date - timedelta(days=30)

            filtered_transactions = insider_transactions[
                (insider_transactions['Date'] >= start_date) & 
                (insider_transactions['Date'] <= end_date)
            ]
            
            if filtered_transactions.empty:
                return "No insider transactions found for the specified date range."
            
            return filtered_transactions.to_csv()
        except Exception as e:
            return f"Error fetching insider transactions for {ticker}: {str(e)}"

    # @tool("Get key financial metrics")
    # def get_key_metrics(ticker):
    #     """
    #     Get key financial metrics for a stock as of 2024-01-01.
    #     The input to this tool should be a ticker.
    #     """
    #     try:
    #         stock = yf.Ticker(ticker)
    #         info = stock.info
            
    #         hist = stock.history(start=Tools.BASE_DATE, end=Tools.BASE_DATE)
    #         if hist.empty:
    #             hist = stock.history(period="1d", end=Tools.BASE_DATE)
            
    #         current_price = hist['Close'].iloc[-1] if not hist.empty else 'N/A'
            
    #         market_cap = info.get('marketCap', 'N/A')
    #         if market_cap != 'N/A':
    #             market_cap = f"{market_cap / 1e9:.1f}"
            
    #         volume = hist['Volume'].iloc[-1] if not hist.empty else 'N/A'
    #         if volume != 'N/A':
    #             volume = f"{volume / 1e6:.1f}"
            
    #         metric = f"""
    #         Key Financial Data (as of {Tools.BASE_DATE}):
            
    #         Bloomberg Ticker: {ticker} US
    #         Sector: {info.get('sector', 'N/A')}
    #         Share Price (USD): {current_price}
    #         Market Cap (USDb): {market_cap}
    #         Volume (m shares): {volume}
    #         Free float (%): {info.get('floatShares', 'N/A') / info.get('sharesOutstanding', 1) * 100:.1f}
    #         Dividend yield (%): {info.get('dividendYield', 0) * 100:.1f}
    #         Net Debt to Equity (%): {info.get('debtToEquity', 'N/A')}
    #         Fwd. P/E (x): {info.get('forwardPE', 'N/A')}
    #         P/Book (x): {info.get('priceToBook', 'N/A')}
    #         ROE (%): {info.get('returnOnEquity', 0) * 100:.1f}
    #         """
    #         return metric
    #     except Exception as e:
    #         return f"Error fetching data for ticker {ticker} as of {Tools.BASE_DATE}: {str(e)}"

# ==== 수정 전 코드 ===== #
# from crewai_tools import tool
# import yfinance as yf

# class Tools:

#     @tool("One month stock price history")
#     def stock_price(ticker):
#         """
#         Useful to get a month's worth of stock price data as CSV.
#         The input of this tool should a ticker, for example AAPL, NET, TSLA etc...
#         """
#         stock = yf.Ticker(ticker)
#         return stock.history(period="1mo").to_csv()

#     @tool("Stock news URLs")
#     def stock_news(ticker):
#         """
#         Useful to get URLs of news articles related to a stock.
#         The input to this tool should be a ticker, for example AAPL, NET
#         """
#         stock = yf.Ticker(ticker)
#         return list(map(lambda x: x["link"], stock.news))
    
#     # 백테스트를 위한 구글 뉴스
#     # def test_stock_news(ticker, date):

# # stock_news("AAPL")
#     @tool("Company's income statement")
#     def income_stmt(ticker):
#         """
#         Useful to get the income statement of a stock as CSV.
#         The input to this tool should be a ticker, for example AAPL, NET
#         """
#         stock = yf.Ticker(ticker)
#         return stock.income_stmt.to_csv()

#     @tool("Balance sheet")
#     def balance_sheet(ticker):
#         """
#         Useful to get the balance sheet of a stock as CSV.
#         The input to this tool should be a ticker, for example AAPL, NET
#         """
#         stock = yf.Ticker(ticker)
#         return stock.balance_sheet.to_csv()

#     @tool("Get insider transactions")
#     def insider_transactions(ticker):
#         """
#         Useful to get insider transactions of a stock as CSV.
#         The input to this tool should be a ticker, for example AAPL, NET
#         """
#         stock = yf.Ticker(ticker)
#         return stock.insider_transactions.to_csv()
    
    # DBS metric 지표를 가져오는 tool 구현
    # @tool("Get key financial metrics")
    # def get_key_metrics(ticker):
    #     """
    #     Useful to get key financial metrics for a stock.
    #     The input to this tool should be a ticker.
    #     """
    #     try:
    #         stock = yf.Ticker(ticker)
    #         info = stock.info
                
    #         market_cap = info.get('marketCap', 'N/A')
    #         if market_cap != 'N/A':
    #             market_cap = f"{market_cap / 1e9:.1f}"  # Convert to billions
                
    #         volume = info.get('volume', 'N/A')
    #         if volume != 'N/A':
    #             volume = f"{volume / 1e6:.1f}"  # Convert to millions
                
    #         # Yahoo Finance Rating: {rating} 제외    
    #         metric = f"""
    #         Key Financial Data:
                
    #         Bloomberg Ticker: {ticker} US
    #         Sector: {info.get('sector', 'N/A')}
    #         Share Price (USD): {info.get('currentPrice', 'N/A')}
    #         12-mth Target Price (USD): {info.get('targetMeanPrice', 'N/A')}
    #         Market Cap (USDb): {market_cap}
    #         Volume (m shares): {volume}
    #         Free float (%): {info.get('floatShares', 'N/A') / info.get('sharesOutstanding', 1) * 100:.1f}
    #         Dividend yield (%): {info.get('dividendYield', 0) * 100:.1f}
    #         Net Debt to Equity (%): {info.get('debtToEquity', 'N/A')}
    #         Fwd. P/E (x): {info.get('forwardPE', 'N/A')}
    #         P/Book (x): {info.get('priceToBook', 'N/A')}
    #         ROE (%): {info.get('returnOnEquity', 0) * 100:.1f}
    #         """
    #         return metric
    #     except Exception as e:
    #         return f"Error fetching data for ticker {ticker}: {str(e)}"