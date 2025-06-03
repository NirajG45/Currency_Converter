import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_URL = "https://open.er-api.com/v6/latest/"

def get_currencies():
    url = API_URL + "USD"
    response = requests.get(url)
    data = response.json()
    print("DEBUG: API response for currencies:", data)
    if data.get("result") == "success":
        return sorted(data["rates"].keys())
    else:
        print("Error fetching currencies:", data.get("error-type", "Unknown error"))
        return []

def get_rates(base_currency):
    url = API_URL + base_currency
    response = requests.get(url)
    data = response.json()
    print("DEBUG: API response for rates:", data)
    if data.get("result") == "success":
        return data["rates"]
    else:
        print("Error fetching rates:", data.get("error-type", "Unknown error"))
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
            rates = get_rates(from_currency)
            if to_currency in rates:
                converted_amount = round(amount * rates[to_currency], 2)
                result = f"{amount} {from_currency} = {converted_amount} {to_currency}"
            else:
                result = "Conversion not supported for selected currency."
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", currencies=currencies, result=result)

if __name__ == "__main__":
    app.run(debug=True)
