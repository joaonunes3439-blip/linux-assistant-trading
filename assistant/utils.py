import re

import pandas as pd
import yfinance as yf


def normalize_symbol(raw: str) -> str:
    text = raw.strip().upper()
    mapping = {
        "BTC": "BTC-USD",
        "BITCOIN": "BTC-USD",
        "ETH": "ETH-USD",
        "ETHEREUM": "ETH-USD",
        "PETR4": "PETR4.SA",
        "PETROBRAS": "PETR4.SA",
        "VALE3": "VALE3.SA",
        "VALE": "VALE3.SA",
        "B3SA3": "B3SA3.SA",
        "B3": "B3SA3.SA",
        "AAPL": "AAPL",
        "MSFT": "MSFT",
    }

    if text in mapping:
        return mapping[text]

    match = re.search(r"[A-Z]{2,5}(?:\.[A-Z]{2,4})?", text)
    if match:
        symbol = match.group(0)
        if "." not in symbol and len(symbol) <= 5:
            return symbol
        return symbol

    return text


def fetch_history(symbol: str, period: str = "30d", interval: str = "1d"):
    ticker = yf.Ticker(normalize_symbol(symbol))
    data = ticker.history(period=period, interval=interval)
    return ticker, data


def get_asset_summary(symbol: str) -> str:
    normalized = normalize_symbol(symbol)
    ticker = yf.Ticker(normalized)
    data = ticker.history(period="5d", interval="1h")

    if data.empty:
        return f"Não foi possível consultar o ativo: {symbol}."

    latest = data.iloc[-1]
    close = float(latest["Close"])
    previous = data.iloc[-2]["Close"] if len(data) > 1 else close
    delta = ((close - previous) / previous) * 100 if previous else 0.0

    return (
        f"Ativo: {normalized}\n"
        f"Preço atual: {close:.2f}\n"
        f"Variação recente: {delta:.2f}%\n"
        f"Último fechamento: {close:.2f}"
    )


def get_signal(symbol: str) -> str:
    try:
        ticker, data = fetch_history(symbol, period="30d", interval="1d")
    except Exception:
        return f"Não foi possível obter o sinal de {symbol}."

    if data.empty:
        return f"Sem dados suficientes para {symbol}."

    data = data.copy()
    data["sma_short"] = data["Close"].rolling(window=5).mean()
    data["sma_long"] = data["Close"].rolling(window=20).mean()

    last_close = float(data["Close"].iloc[-1])
    short = float(data["sma_short"].iloc[-1])
    long = float(data["sma_long"].iloc[-1])

    if short > long:
        signal = "COMPRA"
    elif short < long:
        signal = "VENDA"
    else:
        signal = "HOLD"

    return (
        f"Sinal para {normalize_symbol(symbol)}: {signal}\n"
        f"Preço: {last_close:.2f}\n"
        f"SMA 5: {short:.2f}\n"
        f"SMA 20: {long:.2f}"
    )
