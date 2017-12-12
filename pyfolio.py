import coinmarketcap as c
import json

convertion_currency = 'USD'
price_ = 'price_' + convertion_currency.lower()

def main():
    my_folio, my_folio_total = _refresh()
    print 'My portfolio is:'
    print my_folio
    print 'Total ' + convertion_currency + ' value: ' + str(my_folio_total)

def add(currency, amount):
    currency = currency.lower()
    cmarkap = c.Market()
    coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
    coin_price = float(coin_stats[price_])

    my_folio = _fetch_saved_portfolio()
    if currency in my_folio:
        curr = my_folio[currency]
        curr['amount'] += amount
    else:
        curr = {}
        curr['amount'] = amount

    curr[price_] = float(coin_price)
    curr['total_value'] = curr[price_] * curr['amount']
    my_folio[currency] = curr

    _save_portfolio(my_folio)
    

def remove(currency, amount):
    '''
    Should remove certain amount of currency from portfolio
    reverse of add()
    '''
    pass
    currency = currency.lower()
    cmarkap = c.Market()
    coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
    coin_price = float(coin_stats[price_])

    my_folio = _fetch_saved_portfolio()
    if currency in my_folio:
        curr = my_folio[currency]
        if curr['amount'] < amount:
            print 'You only have {} of {}... '.format(
                str(curr['amount']),
                currency)
            return None
        else:
            curr['amount'] -= amount
    else:
        print 'You have no {} in your portfolio...'.format(currency)
        return None

    curr[price_] = float(coin_price)
    curr['total_value'] = curr[price_] * curr['amount']
    my_folio[currency] = curr

    _save_portfolio(my_folio)


def _total_portfolio_value(my_folio):
    total = 0
    for i in my_folio:
        total += my_folio[i]['total_value']

    return total

def _refresh():
    my_folio = _fetch_saved_portfolio()
    cmarkap = c.Market()

    for i in my_folio:
        currency = i
        # j - is a portfolio entry dict to refresh
        j = my_folio[i]
        coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
        coin_price = float(coin_stats[price_])

        j[price_] = coin_price
        j['total_value'] = j[price_] * j['amount']

        my_folio[i] = j

    _save_portfolio(my_folio)
    total_portfolio_value = _total_portfolio_value(my_folio)
    return my_folio, total_portfolio_value


## TODO
# returns 

#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "pyfolio.py", line 70
#    my_folio_sorted = sorted(my_folio.items(), key=lambda item: item[1][param], reverse)
#SyntaxError: non-keyword arg after keyword ar

#def _sort_portfolio(my_folio, param, reverse=False):
#    my_folio_sorted = sorted(my_folio.items(), key=lambda item: item[1][param], reverse)
#    return my_folio_sorted


def _fetch_saved_portfolio():
    try:
        with open('my_folio.json', 'r') as f:
            my_folio = f.read()
            my_folio_json = json.loads(my_folio)    
    
    except IOError:
        print 'No saved portfolio. New created.'
        my_folio_json = {}
        with open('my_folio.json', 'w+') as f:
            f.write(json.dumps(my_folio_json))

    return my_folio_json

def _save_portfolio(my_folio_json):
    with open('my_folio.json', 'w+') as f:
        f.write(json.dumps(my_folio_json))

if __name__ == '__main__':
    main()
