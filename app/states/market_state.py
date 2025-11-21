import reflex as rx
import yfinance as yf
import pandas as pd
import asyncio
import logging
from datetime import datetime

POPULAR_STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "sector": "Technology"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "sector": "Technology"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical"},
    {"symbol": "META", "name": "Meta Platforms", "sector": "Technology"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
    {"symbol": "AMD", "name": "Advanced Micro Devices", "sector": "Technology"},
    {"symbol": "INTC", "name": "Intel Corp.", "sector": "Technology"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Technology"},
    {"symbol": "ADBE", "name": "Adobe Inc.", "sector": "Technology"},
    {"symbol": "PYPL", "name": "PayPal Holdings", "sector": "Financial Services"},
    {"symbol": "COIN", "name": "Coinbase Global", "sector": "Financial Services"},
    {"symbol": "HOOD", "name": "Robinhood Markets", "sector": "Financial Services"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "sector": "Financial Services"},
    {"symbol": "BAC", "name": "Bank of America", "sector": "Financial Services"},
    {"symbol": "DIS", "name": "Walt Disney Co.", "sector": "Communication Services"},
    {"symbol": "NKE", "name": "Nike Inc.", "sector": "Consumer Cyclical"},
    {"symbol": "SBUX", "name": "Starbucks Corp.", "sector": "Consumer Cyclical"},
]


class MarketState(rx.State):
    search_query: str = ""
    selected_ticker: str = "AAPL"
    current_company_name: str = "Apple Inc."
    current_sector: str = "Technology"
    current_price: float = 0.0
    price_change: float = 0.0
    price_change_percent: float = 0.0
    stock_data: list[dict[str, str | float | int]] = []
    stock_info: dict = {}
    time_range: str = "1mo"
    is_loading: bool = False
    error_message: str = ""
    watchlist: list[str] = ["AAPL", "MSFT", "TSLA", "NVDA"]
    watchlist_data: list[dict[str, str | float | bool]] = []

    @rx.var
    def search_results(self) -> list[dict[str, str]]:
        if not self.search_query:
            return []
        query = self.search_query.lower()
        return [
            s
            for s in POPULAR_STOCKS
            if query in s["symbol"].lower() or query in s["name"].lower()
        ][:5]

    @rx.var
    def is_positive_change(self) -> bool:
        return self.price_change >= 0

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def select_stock(self, symbol: str):
        self.selected_ticker = symbol
        self.search_query = ""
        return MarketState.fetch_stock_data

    @rx.event
    def set_time_range(self, range: str):
        self.time_range = range
        return MarketState.fetch_stock_data

    @rx.event(background=True)
    async def fetch_stock_data(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
        try:
            ticker_symbol = self.selected_ticker
            period = self.time_range
            loop = asyncio.get_running_loop()
            hist = await loop.run_in_executor(
                None, lambda: yf.Ticker(ticker_symbol).history(period=period)
            )
            info = await loop.run_in_executor(
                None, lambda: yf.Ticker(ticker_symbol).info
            )
            async with self:
                data = []
                if not hist.empty:
                    hist = hist.reset_index()
                    for _, row in hist.iterrows():
                        date_str = ""
                        ts = row["Date"]
                        if period in ["1d", "5d"]:
                            date_str = ts.strftime("%H:%M")
                        else:
                            date_str = ts.strftime("%b %d")
                        data.append(
                            {
                                "date": date_str,
                                "price": round(row["Close"], 2),
                                "volume": int(row["Volume"]),
                                "open": round(row["Open"], 2),
                                "high": round(row["High"], 2),
                                "low": round(row["Low"], 2),
                            }
                        )
                self.stock_data = data
                self.stock_info = info
                self.current_company_name = info.get(
                    "shortName", info.get("longName", ticker_symbol)
                )
                self.current_sector = info.get("sector", "N/A")
                if data:
                    last_close = data[-1]["price"]
                    prev_close = info.get("previousClose", data[0]["price"])
                    self.current_price = last_close
                    self.price_change = round(last_close - prev_close, 2)
                    self.price_change_percent = round(
                        self.price_change / prev_close * 100, 2
                    )
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Error fetching stock data: {e}")
            async with self:
                self.error_message = f"Failed to fetch data: {str(e)}"
                self.is_loading = False

    @rx.event(background=True)
    async def update_watchlist_data(self):
        try:
            loop = asyncio.get_running_loop()
            results = []
            async with self:
                current_watchlist = self.watchlist
            for symbol in current_watchlist:
                try:
                    ticker = await loop.run_in_executor(None, lambda: yf.Ticker(symbol))
                    fast_info = await loop.run_in_executor(
                        None, lambda: ticker.fast_info
                    )
                    if fast_info:
                        last_price = fast_info.last_price
                        prev_close = fast_info.previous_close
                        change = last_price - prev_close
                        change_pct = change / prev_close * 100
                        results.append(
                            {
                                "symbol": symbol,
                                "price": round(last_price, 2),
                                "change": round(change, 2),
                                "change_percent": round(change_pct, 2),
                                "is_positive": change >= 0,
                            }
                        )
                except Exception as e:
                    logging.exception(f"Error processing symbol {symbol}: {e}")
                    continue
            async with self:
                self.watchlist_data = results
        except Exception as e:
            logging.exception(f"Watchlist update error: {e}")

    @rx.event
    def add_to_watchlist(self):
        if self.selected_ticker not in self.watchlist:
            self.watchlist.append(self.selected_ticker)
            return MarketState.update_watchlist_data

    @rx.event
    def remove_from_watchlist(self, symbol: str):
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            return MarketState.update_watchlist_data

    @rx.event
    def on_mount(self):
        return [MarketState.fetch_stock_data, MarketState.update_watchlist_data]