import math

from BinanceAPI import BinanceAPI


class trader():

    commission = 0.002

    def __init__(self):
        self.API = BinanceAPI()


    def filters(self, symbol):
        # Get symbol exchange info
        symbol_info = self.API.get_exchange_info(symbol)
        if not symbol_info:
            print('Invalid symbol, please try again...')
            exit(1)
        symbol_info['filters'] = {item['filterType']: item for item in symbol_info['filters']}
        return symbol_info


    def format_step(self, quantity, stepSize):
        return float(stepSize * math.floor(float(quantity)/stepSize))


    def validate(self, symbol, quantity):

        valid = True
        filters = self.filters(symbol)['filters']

        lastBid, lastAsk = self.get_market_price(symbol)

        lastPrice = self.API.get_ticker(symbol)

        minQty = float(filters['LOT_SIZE']['minQty'])
        minPrice = float(filters['PRICE_FILTER']['minPrice'])
        minNotional = float(filters['MIN_NOTIONAL']['minNotional'])
        quantity_temp = float(quantity)

        # stepSize defines the intervals that a quantity/icebergQty can be increased/decreased by.
        stepSize = float(filters['LOT_SIZE']['stepSize'])

        # tickSize defines the intervals that a price/stopPrice can be increased/decreased by
        tickSize = float(filters['PRICE_FILTER']['tickSize'])

        # Just for validation
        lastBid = lastBid + tickSize

        # Set static
        # If quantity or amount is zero, minNotional increase 10%
        if quantity_temp == 0:
	        quantity_temp = (minNotional / lastBid)
	        quantity_temp = quantity_temp + (quantity_temp * 10 / 100)
	        notional = minNotional

        quantity_temp = self.format_step(quantity_temp, stepSize)
        notional = lastBid * float(quantity_temp)

        # minQty = minimum order quantity
        if quantity_temp < minQty:
            print('Invalid quantity, minQty: %.8f (u: %.8f)' % (minQty, quantity_temp))
            valid = False

        if lastPrice < minPrice:
            print('Invalid price, minPrice: %.8f (u: %.8f)' % (minPrice, lastPrice))
            valid = False

        # minNotional = minimum order value (price * quantity)
        if notional < minNotional:
            print('Invalid notional, minNotional: %.8f (u: %.8f)' % (minNotional, notional))
            valid = False

        if not valid:
            return 0, 0

        return quantity_temp, tickSize


    def get_open_trades(self, market):
        order = self.API.get_open_trades(market)
        return order


    def cancel_order(self, market, orderID):
        order = self.API.cancel_order(market, orderID)
        return order


    def get_balance(self, market="BTC"):
        balance = self.API.get_balance(market)
        return balance


    def get_market_price(self, market):
        lastBid, lastAsk = self.API.get_market_price(market)
        return lastBid, lastAsk


    def buy_market(self, market, quantity):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order = self.API.buy_market(market, quantity_validated)    
        return order


    def sell_market(self, market, quantity):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order = self.API.sell_market(market, quantity_validated)    
        return order


    def buy_limit(self, market, quantity, rate):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order = self.API.buy_limit(market, quantity_validated, rate)    
        return order


    def sell_limit(self, market, quantity, rate):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order = self.API.sell_limit(market, quantity_validated, rate)    
        return order


    def sell_OCO_order(self, market, quantity, takeProfitPrice, stopLimit, stopLossPrice):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order = self.API.sell_OCO_order(market, quantity_validated, takeProfitPrice, stopLimit, stopLossPrice)  
        return order


    def calc_decimal_places(self, num):
        count = 0
        temp_num = num
        while temp_num < 1:
            temp_num *= 10
            count += 1
        return count


    def calc_sell_prices(self, lastBid, profitPct, stopLossPct, tickSize):
        takeProfitPrice = lastBid + (lastBid * profitPct / 100) + (lastBid * self.commission)
        stopLossPrice = lastBid - (lastBid * (stopLossPct-self.commission) / 100)
        decimal_places = self.calc_decimal_places(tickSize)
        return round(takeProfitPrice,decimal_places), round(stopLossPrice,decimal_places)


    def trade(self, market, quantity, takeProfitPrice, stopLossPrice):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order1 = self.buy_market(market, quantity_validated)
        stopLimit = float(stopLossPrice) + tickSize
        order2 = self.sell_OCO_order(market, quantity_validated, takeProfitPrice, str(stopLimit), stopLossPrice)
        return order1, order2


    def trade_pct(self, market, quantity, takeProfitPct, stopLossPct):
        quantity_validated, tickSize = self.validate(market, quantity)
        if quantity_validated==0 and tickSize==0:
            return "You encountered a problem! Please try again."
        order1 = self.buy_market(market, quantity_validated)
        lastBid, lastAsk = self.get_market_price(market)
        takeProfitPrice, stopLossPrice = self.calc_sell_prices(lastBid, float(takeProfitPct), float(stopLossPct), tickSize)
        stopLimit = float(stopLossPrice) + tickSize
        order2 = self.sell_OCO_order(market, quantity_validated, str(takeProfitPrice), str(stopLimit), str(stopLossPrice))
        return order1, order2

    def transfer_dust(self, symbol):
        trasnfer = self.API.transfer_dust(symbol)
        return trasnfer

