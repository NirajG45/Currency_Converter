import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "9e5500a9fb2afdc1d7b61e5073e3ee5d"  # Aapki API key yahan daalo

def get_currencies():
    url = f"http://data.fixer.io/api/symbols?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    print("DEBUG: API response for symbols:", data)  # Debug print
    if data.get("success") and "symbols" in data:
        return sorted(data["symbols"].keys())
    else:
        print("Error fetching symbols:", data.get("error", "Unknown error"))
        return []

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
            url = f"http://data.fixer.io/api/convert?access_key={API_KEY}&from={from_currency}&to={to_currency}&amount={amount}"
            response = requests.get(url)
            data = response.json()
            print("DEBUG: API response for conversion:", data)  # Debug print
            if data.get("success") and "result" in data:
                converted_amount = round(data["result"], 2)
                result = f"{amount} {from_currency} = {converted_amount} {to_currency}"
            else:
                error_info = data.get("error", {}).get("info", "Conversion failed")
                result = f"Conversion failed: {error_info}"
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", currencies=currencies, result=result)

@app.route("/test-currencies")
def test_currencies():
    currencies = get_currencies()
    return "<br>".join(currencies) or "No currencies found."

if __name__ == "__main__":
    app.run(debug=True)
