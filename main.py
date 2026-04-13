from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("CURRENCY_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "Webhook is running!"

    try:
        data = request.get_json()
        params = data['queryResult']['parameters']

        source_currency = params['unit-currency']['currency']
        amount = params['unit-currency']['amount']
        target_currency = params['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)

        if cf is None:
            return jsonify({
                "fulfillmentText": "Unable to fetch conversion rate."
            })

        final_amount = round(amount * cf, 2)

        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} = {final_amount} {target_currency}"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "fulfillmentText": "Something went wrong."
        })


def fetch_conversion_factor(source, target):
    try:
        url = f"https://api.currencyapi.com/v3/latest?apikey={"cur_live_BGZDuksi0DbT0zu24hffAPqFT2Bm6LbCnVtSsCBr"}&base_currency={source}&currencies={target}"

        response = requests.get(url).json()

        if 'data' not in response or target not in response['data']:
            print("API Response:", response)
            return None

        return response['data'][target]['value']

    except Exception as e:
        print("API Error:", e)
        return None


if __name__ == "__main__":
    app.run(debug=True)