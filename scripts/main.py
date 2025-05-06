def main():
    # Stock tickers to track
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    # Date range for the data
    start_date = '2020-01-01'
    end_date = '2025-01-01'

    fetcher = AVStockDataFetcher()
    analyzer = StockAnalyzer()
    visualizer = StockVisualizer()
    csv_handler = CSVHandler()
    json_handler = JSONHandler()

if _name__ == "__main__":
    main()
