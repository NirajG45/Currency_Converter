from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Fetch currency list
def get_currencies():
    url = "https://api.exchangerate.host/symbols"
    response = requests.get(url)
    data = response.json()
    return sorted(data["symbols"].keys())

# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    currencies = get_currencies()

    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = request.form["amount"]

        try:
            amount = float(amount)
            url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
            response = requests.get(url)
            data = response.json()
            result = f"{amount} {from_currency} = {data['result']:.2f} {to_currency}"
        except:
            result = "Invalid amount or conversion failed."

    return render_template("index.html", currencies=currencies, result=result)

if __name__ == "__main__":
    app.run(debug=True)
