import requests

def get_exchange_rate(base_currency, target_currency):
    try:
        # You can get a free API key from https://www.exchangerate-api.com/
        API_KEY = "8b4169f1f9635d3b40050a4e"
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency.upper()}"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200 or data["result"] != "success":
            print("❌ Error fetching data from API!")
            print("Message:", data.get("error-type", "Unknown error"))
            return None

        rate = data["conversion_rates"].get(target_currency.upper())
        if rate is None:
            print("❌ Invalid target currency code!")
            return None

        return rate

    except Exception as e:
        print("⚠️ Exception:", e)
        return None


def main():
    print("💱 Live Currency Converter (Powered by ExchangeRate API)")
    base = input("Enter base currency (e.g., USD, INR, EUR): ").upper()
    target = input("Enter target currency (e.g., INR, USD, GBP): ").upper()
    amount = float(input("Enter amount to convert: "))

    rate = get_exchange_rate(base, target)
    if rate:
        converted = amount * rate
        print(f"\n✅ {amount} {base} = {converted:.2f} {target}")
    else:
        print("Conversion failed due to an error.")


if __name__ == "__main__":
    main()
