from flask import Flask, render_template, request, jsonify
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

app = Flask(__name__)
API_URL = "https://api.exchangerate.host"
CURRENCY_SYMBOLS = {}

def fetch_symbols():
    global CURRENCY_SYMBOLS
    response = requests.get(f"{API_URL}/symbols")
    data = response.json()
    if data.get("success", True):
        CURRENCY_SYMBOLS = data["symbols"]
    else:
        CURRENCY_SYMBOLS = {}

def get_exchange_rate(base, target):
    url = f"{API_URL}/latest?base={base}&symbols={target}"
    response = requests.get(url)
    data = response.json()
    if "rates" in data:
        rate = data["rates"].get(target)
        timestamp = data.get("date")
        return rate, timestamp
    return None, None

def get_historical_rates(base, target):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    url = f"{API_URL}/timeseries?start_date={start_date}&end_date={end_date}&base={base}&symbols={target}"
    response = requests.get(url)
    data = response.json()
    if data.get("success"):
        dates = list(data["rates"].keys())
        dates.sort()
        rates = [data["rates"][date][target] for date in dates]
        return dates, rates
    return [], []

@app.route("/", methods=["GET", "POST"])
def index():
    if not CURRENCY_SYMBOLS:
        fetch_symbols()
    result = None
    last_updated = None
    graph_path = None

    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = float(request.form.get("amount", 1))

        rate, last_updated = get_exchange_rate(from_currency, to_currency)
        if rate:
            result = round(rate * amount, 4)

            # Graph creation
            dates, rates = get_historical_rates(from_currency, to_currency)
            if dates and rates:
                plt.figure(figsize=(6, 3))
                plt.plot(dates, rates, marker='o')
                plt.title(f'{from_currency} to {to_currency} (Last 7 Days)')
                plt.xlabel('Date')
                plt.ylabel('Rate')
                plt.xticks(rotation=45)
                plt.tight_layout()
                graph_path = "static/graph.png"
                plt.savefig(graph_path)
                plt.close()

    return render_template("index.html", currencies=CURRENCY_SYMBOLS, result=result,
                           last_updated=last_updated, graph_path=graph_path)

@app.route("/rate", methods=["POST"])
def auto_fetch_rate():
    data = request.json
    base = data.get("base")
    target = data.get("target")
    rate, last_updated = get_exchange_rate(base, target)
    return jsonify({"rate": rate, "last_updated": last_updated})

if __name__ == "__main__":
    app.run(debug=True)
