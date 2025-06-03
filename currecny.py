import requests

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "result" not in data:
            print("Error fetching exchange rate.")
            return None

        result = data['result']
        print(f"\n💱 {amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
        return result

    except Exception as e:
        print("❌ Error:", str(e))
        return None

# Example usage
if __name__ == "__main__":
    print("🌍 Currency Converter")

    from_currency = input("Enter FROM currency (e.g. USD): ").upper()
    to_currency = input("Enter TO currency (e.g. INR): ").upper()
    try:
        amount = float(input("Enter amount: "))
        convert_currency(amount, from_currency, to_currency)
    except ValueError:
        print("❌ Invalid amount entered.")
