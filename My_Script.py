import requests, json, math, time
import alpaca_trade_api as tradeapi
from API_Keys import API_Key_ID, API_Secret_Key

#api = tradeapi.REST()

#API URLs and request headers
Endpoint_Base_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(Endpoint_Base_URL)
POSITIONS_URL = "{}/v2/positions".format(Endpoint_Base_URL)
ORDERS_URL = "{}/v2/orders".format(Endpoint_Base_URL)
ASSETS_URL = "{}/v2/assets".format(Endpoint_Base_URL)

MARKET_DATA = "https://data.alpaca.markets"
LAST_QUOTE_URL = "{}/v1/last_quote/stocks/".format(MARKET_DATA)
LAST_TRADE_URL = "{}/v1/last/stocks/".format(MARKET_DATA)

HEADERS = {'APCA-API-KEY-ID': API_Key_ID, 'APCA-API-SECRET-KEY': API_Secret_Key}

#Functions
#get account info
def get_account(*info):
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    accountinfo = json.loads(r.content)
    return accountinfo


#get open positions
def get_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS)
    positions = json.loads(r.content)
    return positions
    #print("Shares:")
    #for position in positions:
    #    print("{}: {}".format(position['symbol'], position['qty']))

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
    return get_last_quote['last']['askprice']

# get last traded price for an asset
def get_last_trade(symbol_1):
    r = requests.get(LAST_TRADE_URL+symbol_1, headers=HEADERS)
    get_last_trade = json.loads(r.content)
    return get_last_trade['last']['price']

#create a function to view portfolio


#commands
#accountinfo = get_account()
#submitted_orders = get_orders()

breakvar = True
while breakvar == True:
    userInput = input("What do you want to do? \nbuy, sell, portfolio, account, bot, exit \n")

    if userInput == "buy":
        symbol_1 = input("Symbol to buy: ")
        symbol_1 = symbol_1.upper()
        account = get_account()
        info = 'cash'
        amount_to_invest = input("You have $" + str(account[info]) + " and the value of one stock of " + symbol_1 + " is $" + str(get_last_quote(symbol_1)) + ". \nHow much money would you like to invest in this stock?")
        shares_to_buy = math.floor(float(amount_to_invest) / float(get_last_quote(symbol_1)))
        if float(amount_to_invest) > float(account['cash']) or shares_to_buy < 1:
            print("amount to invest: "+amount_to_invest)
            print("cash available for withdrawal: "+account['cash'])
            print("shares to buy: "+str(shares_to_buy))
            print("Not enough funds")
        else:
            #stock_instrument = robinhood_client.instruments(symbol_1)[0]
            print("Queueing shares to buy: "+ str(shares_to_buy))
            #buy_order = create_order("NVDA",1,"buy", "market", "gtc")
            account = get_account()
            print("You have "+account['cash']+" remaining in your account to invest.")
            print("\n")

    elif userInput == "sell":
        positions = get_positions()
        print("Shares:")
        for position in positions:
           print("{}: {}".format(position['symbol'], position['qty']))
        print("\n")

        symbol_to_sell = input("Type a symbol to sell: ")
        shares_to_sell = input("Number of shares to sell: ")
        symbol_to_sell = symbol_to_sell.upper()

        sell_order = create_order(symbol_to_sell,shares_to_sell,"sell", "market", "gtc")

    elif userInput == "portfolio":
        positions = get_positions()
        print("Shares:")
        for position in positions:
            print("{}: {}".format(position['symbol'], position['qty']))

        print(positions)
        print("\n")

    elif userInput == "account":
         accountinfo = get_account();
         for n in accountinfo: print(n+": "+str(accountinfo[n])) #get account info,
         print("\n")

    elif userInput == "bot":
        symbol_1 = input("Symbol to buy: ")
        symbol_1 = symbol_1.upper()
        price_decrease = float(input("buy at what % price decrease (1): ")) / 100
        position_increase = input("shares to buy if price goes down (1): ")
        price_increase = float(input("sell at what % profit (10): ")) / 100
        # position_decrease = input("shares to sell if price goes up: ")  #the optimal is to sell all shares

        # makes the initial buy:
        buy_order = create_order(symbol_1,1,"buy", "market", "gtc")
        print("Bought start share: " + symbol_1)

        # track vars:
        # get cost of stock
        results = get_positions()  # 1. this is a list of securities
        print(results)
        for security in results:  # credit: David security represents the ith element in the results array.
            if security['symbol'] == symbol_1:  # if dict key "symbol" == the symbol we're trading:
                # print cost of stock:
                average_buy_price = float(security['avg_entry_price'])
                shares_owned = security['qty']
                print(symbol_1 + " average buy price: " + str(average_buy_price) + ", " + shares_owned)

        # loop each minute until updated time does not change 3 times. <-----
        # get current market price of stock and time
        # consider do while loop or while true
        previous_time = 0
        previous_price = 74  # CHANGE TO ZERO WHEN YOU FIX THE ERROR HANDLING OF ZEROS
        counter = 0
        # shares_owned = security['quantity']
        log_previous_time = []
        log_decision = []
        log_ask_price = []
        log_shares_owned = []
        print("time, ask, Average buy price, decision, shares")

        while counter < 5:
            updated_at = get_last_quote(symbol_1)
            ask_price = get_last_quote(symbol_1)
            decision = "hold"


            if updated_at == previous_time:
                counter += 1

            previous_time = updated_at

            # add block to check if there are already unsold shares from the previous day, and so therefore to NOT buy more shares.

            # decide to buy, sell or hold
            if (ask_price / previous_price) - 1 <= -price_decrease:  # buy if
                # except ZeroDivisionError:
                # pass
                print(
                    'average buy price (' + str(average_buy_price) + ') > ask price (' + str(ask_price) + '), so will buy.')
                buy_order = create_order(symbol_1,position_increase,"buy", "market", "gtc")
                print('new average buy price: ' + str(average_buy_price))  # this is printing the old var value.  it needs to query to get the new value.

                previous_price = ask_price
                shares_owned = security['qty']
                decision = "buy"

            elif (ask_price / average_buy_price) - 1 >= price_increase:  # sell if
                print('average buy price (' + str(average_buy_price) + ') < ask price (' + str(ask_price) + '), so will sell.')
                sell_order = create_order(symbol_1,shares_owned,"sell", "market", "gtc")
                print('new average buy price: ' + str(average_buy_price))
                decision = "sell all and stop"
                breakvar = False

            log_previous_time.append(previous_time)
            log_decision.append(decision)
            log_ask_price.append(ask_price)
            log_shares_owned.append(shares_owned)
            print(str(previous_time) + " , " + str(ask_price) + ", " + str(average_buy_price) + ", " + str(decision) + ", " + str(shares_owned))
            time.sleep(2)

    elif userInput == "exit":
        print("Good bye!")
        breakvar = False