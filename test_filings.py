from cad_tickers.sedar.tsx import get_ticker_filings, get_news_and_events

filings = get_ticker_filings("BRAG")

print(filings)