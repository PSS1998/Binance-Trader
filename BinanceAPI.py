from binance.client import Client
from binance.enums import *

import config


class BinanceAPI:

    def __init__(self):
        self.client = Client(config.api_key, config.api_secret)

    def get_open_trades(self, market):
        order = self.client.get_open_orders(symbol=market)
        return order

    def cancel_order(self, market, orderID):
        order = self.client.cancel_order(
            symbol=market,
            orderId=orderID)
        return order

    def get_balance(self, market="BTC"):
        balance = self.client.get_asset_balance(asset=market)
        balance = balance['free']
        return balance

    def get_market_price(self, market):
        depth = self.client.get_order_book(symbol=market, limit=5)
        lastBid = float(depth['bids'][0][0]) #last buy price (bid)
        lastAsk = float(depth['asks'][0][0]) #last sell price (ask)
        return lastBid, lastAsk

    def buy_market(self, market, quantity):
        order = self.client.order_market_buy(
            symbol=market,
            quantity=quantity)    
        return order

    def sell_market(self, market, quantity):
        order = self.client.order_market_sell(
            symbol=market,
            quantity=quantity)    
        return order

    def buy_limit(self, market, quantity, rate):
        order = self.client.order_limit_buy(
            symbol=market,
            quantity=quantity,
            price=rate)    
        return order

    def sell_limit(self, market, quantity, rate):
        order = self.client.order_limit_sell(
            symbol=market,
            quantity=quantity,
            price=rate)    
        return order

    def sell_OCO_order(self, market, quantity, takeProfitPrice, stopLimit, stopLossPrice):
        order = self.client.create_oco_order(
            symbol=market,
            side=SIDE_SELL,
            quantity=quantity,
            stopLimitTimeInForce=TIME_IN_FORCE_GTC,
            price=takeProfitPrice,
            stopPrice=stopLimit,
            stopLimitPrice=stopLossPrice
            )    
        return order

    def get_exchange_info(self, symbol):
        info = self.client.get_exchange_info()
        if symbol != "":
            return [market for market in info['symbols'] if market['symbol'] == symbol][0]
        return info

    def get_ticker(self, market):
        ticker = self.client.get_ticker(symbol=market)
        return float(ticker['lastPrice'])












