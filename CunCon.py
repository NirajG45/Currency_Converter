import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "9e5500a9fb2afdc1d7b61e5073e3ee5d"  # Your API key here

def get_currencies():
    url = f"http://data.fixer.io/api/symbols?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("success") and "symbols" in data:
        return sorted(data["symbols"].keys())
    else:
        print("API response error:", data)
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    currencies = get_currencies()

    if request.method == "POST":
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")
        amount = request.form.get("amount")

        try:
            amount = float(amount)
            url = f"http://data.fixer.io/api/convert?access_key={API_KEY}&from={from_currency}&to={to_currency}&amount={amount}"
            response = requests.get(url)
            data = response.json()
            if data.get("success") and "result" in data:
                converted = round(data["result"], 2)
                result = f"{amount} {from_currency} = {converted} {to_currency}"
            else:
                result = "Conversion failed. Please try again later."
        except Exception as e:
            result = f"Error: {e}"

    return render_template("index.html", currencies=currencies, result=result)

if __name__ == "__main__":
    app.run(debug=True)
