import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "9719b709bc98994bcad4ea28"  # Your API key here

def get_currencies():
    url = f"http://data.fixer.io/api/symbols?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    print("DEBUG: API response for symbols:", data)
    if data.get("success") and "symbols" in data:
        return sorted(data["symbols"].keys())
    else:
        print("Error fetching symbols:", data.get("error", "Unknown error"))
        return []

def get_latest_rates(base="EUR"):
    url = f"http://data.fixer.io/api/latest?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    print("DEBUG: API response for latest rates:", data)
    if data.get("success") and "rates" in data:
        return data["rates"]
    else:
        print("Error fetching latest rates:", data.get("error", "Unknown error"))
        return {}

@app.route("/", methods=["GET", "POST"])
def index():
    currencies = get_currencies()
    result = None

    if request.method == "POST":
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")
        amount = request.form.get("amount")

        try:
            amount = float(amount)
            rates = get_latest_rates()

            # Fixer free plan base currency is EUR
            if from_currency not in rates or to_currency not in rates:
                result = "Conversion not supported for selected currency."
            else:
                # Convert amount to EUR first, then to target currency
                amount_in_eur = amount / rates[from_currency]
                converted_amount = amount_in_eur * rates[to_currency]
                converted_amount = round(converted_amount, 2)
                result = f"{amount} {from_currency} = {converted_amount} {to_currency}"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", currencies=currencies, result=result)

if __name__ == "__main__":
    app.run(debug=True)
