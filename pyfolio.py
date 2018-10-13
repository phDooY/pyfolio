import coinmarketcap as c
import json
import pandas as pd
from text2png import text2png

portfolios_folder = 'portfolios'

convertion_currency = 'USD'
price_ = 'price_' + convertion_currency.lower()

def main(telegram_uid):
    #try:
    my_folio, my_folio_total = _refresh(telegram_uid)
    #except:
    #return None
    if not my_folio:
        return None
    my_folio_table = _pd_sort_and_print(my_folio, telegram_uid)
    #print 'My portfolio is ({} values):'.format(convertion_currency)
    #print my_folio_table
    #return 'My portfolio ({} values):\n'.format(convertion_currency) + '```' + my_folio_table.to_string() + '\n```'
    reply =  'My portfolio ({} values):\n'.format(convertion_currency) + my_folio_table.to_string()
    picture_location = portfolios_folder + '/' + str(telegram_uid) + '.png'
    text2png(reply, picture_location)
    return picture_location

def add(currency, amount, telegram_uid):
    currency = currency.lower()
    cmarkap = c.Market()
    coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
    coin_price = float(coin_stats[price_])

    my_folio = _fetch_saved_portfolio(telegram_uid)
    if currency in my_folio:
        curr = my_folio[currency]
        curr['amount'] += amount
    else:
        curr = {}
        curr['amount'] = amount

    curr[price_] = float(coin_price)
    curr['total_value'] = curr[price_] * curr['amount']
    my_folio[currency] = curr

    _save_portfolio(my_folio, telegram_uid)
    

def remove(currency, amount, telegram_uid):
    '''
    Should remove certain amount of currency from portfolio
    reverse of add()
    '''
    currency = currency.lower()
    cmarkap = c.Market()
    coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
    coin_price = float(coin_stats[price_])

    my_folio = _fetch_saved_portfolio(telegram_uid)
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

    _save_portfolio(my_folio, telegram_uid)


def _total_portfolio_value(my_folio):
    total = 0
    for i in my_folio:
        total += my_folio[i]['total_value']

    return total

def _refresh(telegram_uid):
    my_folio = _fetch_saved_portfolio(telegram_uid)
    cmarkap = c.Market()

    for i in my_folio:
        currency = i
        # j - is a portfolio entry dict to refresh
        j = my_folio[i]
        print currency, convertion_currency
        coin_stats = cmarkap.ticker(currency, convert=convertion_currency)[0]
        coin_price = float(coin_stats[price_])

        j[price_] = coin_price
        j['total_value'] = j[price_] * j['amount']

        my_folio[i] = j

    _save_portfolio(my_folio, telegram_uid)
    total_portfolio_value = _total_portfolio_value(my_folio)
    return my_folio, total_portfolio_value


def _pd_sort_and_print(my_folio, telegram_uid):
    portfolio_name = str(telegram_uid)
    # reads JSON into DataFrame object
    df = pd.read_json('{}/{}.json'.format(portfolios_folder, portfolio_name))
    # transpose df
    df = df.transpose()
    # sort and select columns
    df = df[['amount', 'price_usd', 'total_value']].sort_values(['total_value'], ascending=False)
    # define total sum row
    sum_row = {col: df[col].sum() if col == 'total_value' else None for col in df}
    # Turn the sums into a DataFrame with one row with an index of 'Total':
    sum_df = pd.DataFrame(sum_row, index=["Total"])
    # Now append the row:
    df = df.append(sum_df)

    # here trying to convert format to markdown
    # taken from https://stackoverflow.com/questions/33181846/programmatically-convert-pandas-dataframe-to-markdown-table

#    cols = df.columns
#    df2 = pd.DataFrame([['---',]*len(cols)], columns=cols)

    #Create a new concatenated DataFrame
#    df3 = pd.concat([df2, df])

    return df


# TODO
# as long as I am using pandas, maybe makes sense to do all 
# data wrangling with pandas
def _sort_portfolio(my_folio, param, reverse=False):
    my_folio_sorted = sorted(my_folio.items(), key=lambda item: item[1][param], reverse=reverse)
    return my_folio_sorted


def _fetch_saved_portfolio(telegram_uid):
    portfolio_name = str(telegram_uid)
    try:
        with open('{}/{}.json'.format(portfolios_folder, portfolio_name), 'r') as f:
            my_folio = f.read()
            my_folio_json = json.loads(my_folio)    
    
    except IOError:
        print 'No saved portfolio. New created.'
        my_folio_json = {}
        with open('{}/{}.json'.format(portfolios_folder, portfolio_name), 'w+') as f:
            f.write(json.dumps(my_folio_json))

    return my_folio_json

def _save_portfolio(my_folio_json, telegram_uid):
    portfolio_name = str(telegram_uid)
    with open('{}/{}.json'.format(portfolios_folder, portfolio_name), 'w+') as f:
        f.write(json.dumps(my_folio_json))

if __name__ == '__main__':
    main()
