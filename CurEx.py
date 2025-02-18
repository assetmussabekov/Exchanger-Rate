from flask import *
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_URL = "https://fast-price-exchange-rates.p.rapidapi.com/api/v1/convert"
HEADERS = {
    "x-rapidapi-key": "437803c4bcmsh06f4b6476fadb03p17d2eajsn334946f683c8",
    "x-rapidapi-host": "fast-price-exchange-rates.p.rapidapi.com"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    source_currency = request.form['source_currency']
    target_currency = request.form['target_currency']
    amount = float(request.form['amount'])

    querystring = {"base_currency": source_currency, "quote_currency": target_currency}
    response = requests.get(API_URL, headers=HEADERS, params=querystring)
    data = response.json()

    exchange_rate = data.get('rate')
    if exchange_rate:
        result = amount * exchange_rate
    else:
        result = 'Ошибка получения курса'

    if 'history' not in session:
        session['history'] = []
    session['history'].append({
        'source_currency': source_currency,
        'target_currency': target_currency,
        'amount': amount,
        'result': result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    if len(session['history']) > 5:
        session['history'].pop(0)

    return render_template('index.html', result=result, exchange_rate=exchange_rate)


@app.route('/history')
def history():
    return render_template('history.html', history=session.get('history', []))


@app.route('/clear_history')
def clear_history():
    session.pop('history', None)
    return redirect(url_for('index'))


@app.route('/exchange_rate')
def exchange_rate():
    base_currencies = ['USD', 'EUR', 'CNY', 'GBP', 'UZS', 'RUB']
    rates = {}
    for base_currency in base_currencies:
        querystring = {"base_currency": base_currency}
        response = requests.get(API_URL, headers=HEADERS, params=querystring)
        if response.status_code == 200:
            rates[base_currency] = response.json().get('rates', {})
        else:
            rates[base_currency] = "Ошибка получения данных"
    return render_template('exchange_rate.html', rates=rates)

if __name__ == '__main__':
    app.run(debug=False)
