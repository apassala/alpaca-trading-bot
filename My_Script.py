import requests, json
import alpaca_trade_api as tradeapi
from API_Keys import API_Key_ID, API_Secret_Key

#api = tradeapi.REST()

#API URLs and request headers
Endpoint_Base_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(Endpoint_Base_URL)
ORDERS_URL = "{}/v2/orders".format(Endpoint_Base_URL)
ASSETS_URL = "{}/v2/assets".format(Endpoint_Base_URL)

MARKET_DATA = "https://data.alpaca.markets"
LAST_QUOTE_URL = "{}/v1/last_quote/stocks/".format(MARKET_DATA)
LAST_TRADE_URL = "{}/v1/last/stocks/".format(MARKET_DATA)

HEADERS = {'APCA-API-KEY-ID': API_Key_ID, 'APCA-API-SECRET-KEY': API_Secret_Key}

#Functions
#get account info
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    accountinfo = json.loads(r.content)
    return accountinfo

#buy or sell depending on side = "buy" or "sell"
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,  #'market'
        "time_in_force": time_in_force #'gtc'
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

#response = create_order("NVDA",1,"buy", "market", "gtc")
#print(response)

#see your posted orders
def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
    get_order = json.loads(r.content)
    return get_order

#get assets available to trade but not market data
def get_assets(symbol_1):
    r = requests.get(ASSETS_URL+"/"+symbol_1, headers=HEADERS)
    get_assets = json.loads(r.content)
    return get_assets

#get last quoted price for an asset
def get_last_quote(symbol_1):
    r = requests.get(LAST_QUOTE_URL+symbol_1, headers=HEADERS)
    get_last_quote = json.loads(r.content)
    print(get_last_quote)
    # last_quote = json.loads(r.content)
    # return last_quote

def get_last_trade(symbol_1):
    r = requests.get(LAST_TRADE_URL+symbol_1, headers=HEADERS)
    print(LAST_TRADE_URL+symbol_1)
    print(r)
    # last_quote = json.loads(r.content)
    # return last_quote

#create a function to view portfolio

#commands
accountinfo = get_account()
submitted_orders = get_orders()

# breakvar = True
# while breakvar == True:
#     userInput = input("What do you want to do? \nbuy, sell, portfolio, account, bot, exit \n")
#
#     if userInput == "buy":
#         symbol_1 = input("Symbol to buy: ")
#         symbol_1 = symbol_1.upper()
#         cash_available_for_withdrawal = accountinfo['cash']
#         amount_to_invest = input("You have " + accountinfo[
#             'cash'] + " and the value of one stock of " + symbol_1 + " is " + symbol_data[
#                                      'ask_price'] + ". How much money would you like to invest in this stock?")
last_quote = get_last_trade('AAPL')
print('last quote: ' + str(last_quote))