import yfinance as yf
import pandas as pd

class Tools:
    def stock_price(self, ticker, start_date, end_date):
        """
        Get stock price data for a custom date range as CSV.
        The input should be a ticker (e.g., AAPL, NET, TSLA) and date range (start_date, end_date).
        """
        stock = yf.Ticker(ticker)
        return stock.history(start=start_date, end=end_date).to_csv()

    def stock_news(self, ticker):
        """
        Useful to get URLs of news articles related to a stock.
        The input to this tool should be a ticker, for example AAPL, NET
        """
        stock = yf.Ticker(ticker)
        return list(map(lambda x: x["link"], stock.news))

    def income_stmt(self, ticker, date):
        """
        Get the income statement of a stock for a specific date as CSV.
        The input should be a ticker (e.g., AAPL, NET) and date (YYYY-MM-DD).
        """
        stock = yf.Ticker(ticker)
        print(f"CHECK_VARS:{vars(stock)}")
        financials = stock.financials
        # 필터링하여 특정 날짜의 데이터만 추출
        filtered_financials = financials.loc[:, financials.columns == date]
        return filtered_financials.to_csv()

    def balance_sheet(self, ticker, date):
        """
        Get the balance sheet of a stock for a specific date as CSV.
        The input should be a ticker (e.g., AAPL, NET) and date (YYYY-MM-DD).
        """
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet
        # 필터링하여 특정 날짜의 데이터만 추출
        filtered_balance_sheet = balance_sheet.loc[:, balance_sheet.columns == date]
        return filtered_balance_sheet.to_csv()

    def insider_transactions(self, ticker, start_date=None, end_date=None):
        """
        Get insider transactions of a stock for a custom date range as CSV.
        The input should be a ticker (e.g., AAPL, NET) and optional date range (start_date, end_date).
        If start_date is None, the earliest available data is used.
        """
        stock = yf.Ticker(ticker)
        insider_transactions = stock.insider_transactions
        
        # Convert 'Start Date' to datetime
        insider_transactions['Start Date'] = pd.to_datetime(insider_transactions['Start Date'])
        
        # If start_date is None, use the earliest date available
        if start_date is None:
            start_date = insider_transactions['Start Date'].min()
        
        # If end_date is None, use the latest date available
        if end_date is None:
            end_date = insider_transactions['Start Date'].max()

        # 날짜를 기준으로 필터링
        filtered_transactions = insider_transactions[
            (insider_transactions['Start Date'] >= start_date) & 
            (insider_transactions['Start Date'] <= end_date)
        ]
        return filtered_transactions.to_csv()

# 툴을 활용하기 위한 클래스 인스턴스 생성
tools = Tools()

# 원하는 날짜 범위를 설정 (예: 2023-01-01 부터 2023-02-01)
start_date = "2023-01-01"
end_date = "2023-02-01"
specific_date = "2023-09-30"

# 주식 가격 데이터 추출 (예: Apple Inc.)
stock_price_data = tools.stock_price("AAPL", start_date, end_date)
print("Stock Price Data:\n", stock_price_data)

# 관련 뉴스 URL 추출 (예: Apple Inc.)
stock_news_urls = tools.stock_news("AAPL")
print("Stock News URLs:\n", stock_news_urls)

# 잔고표 데이터 추출 (예: Apple Inc.)
balance_sheet_data = tools.balance_sheet("AAPL", specific_date)
print("Balance Sheet Data:\n", balance_sheet_data)

# 내부자 거래 데이터 추출 (예: Apple Inc.)
insider_transactions_data = tools.insider_transactions("AAPL", start_date, end_date)
print("Insider Transactions Data:\n", insider_transactions_data)

# 소득 명세서 데이터 추출 (예: Apple Inc.)
income_statement_data = tools.income_stmt("AAPL", specific_date)
print("Income Statement Data:\n", income_statement_data)

# 내부자 거래 데이터 추출 (start_date 지정하지 않음)
all_insider_transactions_data = tools.insider_transactions("AAPL")
print("All Insider Transactions Data:\n", all_insider_transactions_data)
