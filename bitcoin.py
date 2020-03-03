"""
Use the Coindesk API to convert dollars to Bitcoin
https://www.coindesk.com/coindesk-api

Attribution: 
This app powered by CoinDesk, https://www.coindesk.com/price/bitcoin

"""

import requests 

coinbase_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'

def main():
    dollars = get_dollars()
    try:
        bitcoin = convert_dollars_to_bitcoin(dollars, coinbase_url)
        display(dollars, bitcoin)
    except BitCoinError as e:
        print(f'Error converting. Reason: {e}')


def get_dollars():

    """ Get a positive number from the user """
    while True:
        try:
            dollars = float(input('Enter dollars: '))
            if dollars >= 0:
                return dollars
            else:
                print('Enter a positive number')
        except ValueError:
            print('Enter a number')


def convert_dollars_to_bitcoin(dollars, url):
    json = api_call(url)
    rate = get_bitcoin_rate_float(json)
    bitcoin = convert(dollars, rate)
    return bitcoin


def api_call(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises an exception if there is an error e.g. 404 not found
        return response.json()
    except Exception as e:
        raise BitCoinError(f'Error making request to CoinDesk') from e
    

def get_bitcoin_rate_float(json):
    try:
        bpi = json['bpi']
        us = bpi['USD']
        rate_float = us['rate_float']
        return rate_float
    except Exception as e:
        raise BitCoinError('Could not process response from CoinDesk') from e


def convert(dollars, rate):
    return dollars * rate


def display(dollars, bitcoin):
    print(f'Today, ${dollars:.2f} is equivalent to {bitcoin:.2f}')


class BitCoinError(Exception):
    pass 

if __name__ == '__main__':
    main()