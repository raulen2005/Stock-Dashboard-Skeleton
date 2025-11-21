import reflex as rx
import yfinance as yf
import pandas as pd
import asyncio
import logging
from datetime import datetime

POPULAR_STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Tecnología"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "sector": "Tecnología"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Tecnología"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumo Cíclico"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "sector": "Tecnología"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumo Cíclico"},
    {"symbol": "META", "name": "Meta Platforms", "sector": "Tecnología"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Servicios de Comunicación"},
    {"symbol": "AMD", "name": "Advanced Micro Devices", "sector": "Tecnología"},
    {"symbol": "INTC", "name": "Intel Corp.", "sector": "Tecnología"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Tecnología"},
    {"symbol": "ADBE", "name": "Adobe Inc.", "sector": "Tecnología"},
    {"symbol": "PYPL", "name": "PayPal Holdings", "sector": "Servicios Financieros"},
    {"symbol": "COIN", "name": "Coinbase Global", "sector": "Servicios Financieros"},
    {"symbol": "HOOD", "name": "Robinhood Markets", "sector": "Servicios Financieros"},
    {"symbol": "JPM", "name": "JPMorgan Chase", "sector": "Servicios Financieros"},
    {"symbol": "BAC", "name": "Bank of America", "sector": "Servicios Financieros"},
    {"symbol": "DIS", "name": "Walt Disney Co.", "sector": "Servicios de Comunicación"},
    {"symbol": "NKE", "name": "Nike Inc.", "sector": "Consumo Cíclico"},
    {"symbol": "SBUX", "name": "Starbucks Corp.", "sector": "Consumo Cíclico"},
]


class MarketState(rx.State):
    search_query: str = ""
    selected_ticker: str = "AAPL"
    current_company_name: str = "Apple Inc."
    current_sector: str = "Tecnología"
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
    comparison_symbols: list[str] = []
    available_symbols: list[str] = [s["symbol"] for s in POPULAR_STOCKS]
    colors: list[str] = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD"]
    hover_date: str = ""
    hover_price: str = ""

    @rx.event
    def set_hover_data(self, data: dict):
        if data and "activePayload" in data and data["activePayload"]:
            self.hover_date = data["activeLabel"]
            try:
                payload = data["activePayload"][0]["payload"]
                price = payload.get("price")
                self.hover_price = str(price) if price is not None else ""
            except (KeyError, IndexError, TypeError) as e:
                logging.exception(f"Error processing hover data: {e}")
                self.hover_price = ""
        else:
            self.hover_date = ""
            self.hover_price = ""

    @rx.event
    def clear_hover_data(self):
        self.hover_date = ""
        self.hover_price = ""

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
    def toggle_comparison(self, symbol: str):
        if symbol == self.selected_ticker:
            return
        if symbol in self.comparison_symbols:
            self.comparison_symbols.remove(symbol)
        else:
            self.comparison_symbols.append(symbol)
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
            main_hist = await loop.run_in_executor(
                None, lambda: yf.Ticker(ticker_symbol).history(period=period)
            )
            info = await loop.run_in_executor(
                None, lambda: yf.Ticker(ticker_symbol).info
            )
            data = []
            if not main_hist.empty:
                main_hist = main_hist.reset_index()
                comparison_data = {}
                async with self:
                    comp_syms = self.comparison_symbols
                for sym in comp_syms:
                    comp_hist = await loop.run_in_executor(
                        None, lambda: yf.Ticker(sym).history(period=period)
                    )
                    if not comp_hist.empty:
                        comp_hist = comp_hist.reset_index()
                        comparison_data[sym] = comp_hist
                for _, row in main_hist.iterrows():
                    date_val = row["Date"]
                    date_str = ""
                    if period in ["1d", "5d"]:
                        date_str = date_val.strftime("%H:%M")
                    else:
                        date_str = date_val.strftime("%b %d")
                    point = {
                        "date": date_str,
                        "price": round(row["Close"], 2),
                        "volume": int(row["Volume"]),
                        "open": round(row["Open"], 2),
                        "high": round(row["High"], 2),
                        "low": round(row["Low"], 2),
                    }
                    for sym, hist_df in comparison_data.items():
                        match = hist_df[hist_df["Date"] == date_val]
                        if not match.empty:
                            point[sym] = round(match.iloc[0]["Close"], 2)
                        else:
                            point[sym] = None
                    data.append(point)
            async with self:
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
                self.error_message = f"Error al obtener datos: {str(e)}"
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