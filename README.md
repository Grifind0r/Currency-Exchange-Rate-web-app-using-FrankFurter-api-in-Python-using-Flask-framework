# Currency-Exchange-Rate-web-app-using-FrankFurter-api-in-Python-using-Flask-framework
# Currency Converter Project

This project involves a simple currency converter that utilizes the [Frankfurter API](https://www.frankfurter.app/).

## Code Overview

```python
# Import necessary libraries
import requests
import json
import datetime
import numpy as np

# Function to check if the API is working correctly and get a list of currencies
def get_curr():
    checkapi = False
    try:
        currencies = requests.get("https://api.frankfurter.app/currencies")
        new = currencies.json()
    except ValueError:
        checkapi = True
    cList = list(new.keys())
    return cList, checkapi

# Function to check if the provided currencies are in the Frankfurter supported currencies
def check_currencies(from_c, to_c, cList):
    currency1Exist, currency2Exist = False, False

    if from_c.upper() in cList:
        currency1Exist = True
    if to_c.upper() in cList:
        currency2Exist = True

    return currency1Exist, currency2Exist

# Function to check if the provided date is correct
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

# Function to convert currency using the Frankfurter API
def convert_currency(date, from_c, to_c):
    currency1Exist = False
    currency2Exist = False
    apiError = False
    cList, apiError = get_curr()

    currency1Exist, currency2Exist = check_currencies(from_c, to_c, cList)
    correctDate = check_date(date)

    if correctDate and currency1Exist and currency2Exist and not apiError:
        amount = 1

        # API call to get exchange rate from 'from_c' to 'to_c'
        response1 = requests.get(
            f"https://api.frankfurter.app/{date}?amount={amount}&from={from_c}&to={to_c}"
        )

        # API call to get exchange rate from 'to_c' to 'from_c'
        response2 = requests.get(
            f"https://api.frankfurter.app/latest?amount={amount}&from={to_c}&to={from_c}"
        )

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
            return "There is an error with the Frankfurter API"
        elif not currency1Exist and not currency2Exist:
            return f"{from_c} and {to_c} are not valid currency codes"

# Prompts user about the available currencies and asks for date, from currency, and to currency
print('Select from these currencies:', get_curr()[0])
date = input("Enter date:")
from_c = input("From:")
to_c = input("To:")
convert_currency(date, from_c, to_c)
