from flask import Flask, render_template, request
import requests
import datetime
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        date = request.form['date']
        from_c = request.form['from_currency']
        to_c = request.form['to_currency']
        result = convert_currency(date, from_c, to_c)

    return render_template('index.html', result=result)
def check_currencies(from_c, to_c):
    currency1Exist, currency2Exist, apiError = False, False, False

    try:
        currencies = requests.get("https://api.frankfurter.app/currencies")
        currency_data = currencies.json()
    except ValueError:
        apiError = True

    cList = list(currency_data.keys())

    if from_c.upper() in cList:
        currency1Exist = True
    if to_c.upper() in cList:
        currency2Exist = True

    return currency1Exist, currency2Exist, apiError

def check_date(date):
    correctDate = None
    x = date.split("-")

    if len(x) == 3:
        try:
            newDate = datetime.date(int(x[0]), int(x[1]), int(x[2]))
            correctDate = True
        except ValueError:
            correctDate = False
    else:
        correctDate = False

    return correctDate

def convert_currency(date, from_c, to_c):
    currency1Exist, currency2Exist, apiError = check_currencies(from_c, to_c)
    correctDate = check_date(date)

    if correctDate and currency1Exist and currency2Exist and not apiError:
        amount = 1

        response1 = requests.get(
            f"https://api.frankfurter.app/{date}?amount={amount}&from={from_c}&to={to_c}")
        response2 = requests.get(
            f"https://api.frankfurter.app/latest?amount={amount}&from={to_c}&to={from_c}")

        Dict1 = response1.json()
        Dict2 = response2.json()
        rate1 = list(Dict1["rates"].values())[0]
        rate2 = list(Dict2["rates"].values())[0]

        return (
            f"The conversion rate on {date} from {Dict1['base']} to {to_c} was {rate1}. "
            f"The inverse rate was {rate2}"
        )
    else:
        if not correctDate:
            return "Provided date is invalid"
        elif not currency1Exist and currency2Exist:
            return f"{from_c} is not a valid currency code"
        elif currency2Exist and not currency1Exist:
            return f"{to_c} is not a valid currency code"
        elif apiError:
            return "This is an error with the Frankfurter API"
        elif not currency1Exist and not currency2Exist:
            return f"{from_c} and {to_c} are not valid currency codes"

if __name__ == '__main__':
    app.run(debug=True)
