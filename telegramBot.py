import subprocess
import configparser
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from collections import defaultdict

import config
from trader import trader


helpMessage = '''
Below you can see all the commands:

Buy_market --market market --quantity quantity
Sell_market --market market --quantity quantity
Buy_limit --market market'] --quantity quantity --rate rate
Sell_limit --market market'] --quantity quantity --rate rate
Get_open_trades --market market
Cancel_order --market market --orderID orderID
Get_balance --market market
Get_market_price --market market
Sell_OCO_order --market market --quantity quantity --takeProfitPrice takeProfitPrice --stopLimit stopLimit --stopLossPrice stopLossPrice
Trade --market market --quantity quantity --takeProfitPrice takeProfitPrice --stopLossPrice stopLossPrice
Trade_pct --market market --quantity quantity --takeProfitPct takeProfitPct --stopLossPct stopLossPct

*you can also use amount of BTC instead of quantity (--amount amount)
*for get_balance market argument is optional
*if you dont use amount or quantity minimum quantity will be used
'''


### Get admin chat_id from config file
### For more security replies only send to admin chat_id
adminCID = config.telegram_admin_chatID

### Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


trader_class = trader()

### This function run command and send output to user
def runCMD(bot, update):
    if not isAdmin(bot, update):
        return
    try:
        usercommand = update.message.text
        usercommand = usercommand.split()
        options = defaultdict()
        response = ""
        for i in range(1, len(usercommand), 2):
            options[usercommand[i][2:]] = usercommand[i+1]
        
        if 'quantity' not in options:
            if 'amount' in options:
                lastBid, lastAsk = trader_class.get_market_price(options['market'])
                options['quantity'] = (float(options['amount']) / lastBid)
            else:
                options['quantity'] = '0'
        
        if(usercommand[0] == "Buy_market"):
            response = trader_class.buy_market(options['market'], float(options['quantity']))
        elif(usercommand[0] == "Sell_market"):
            response = trader_class.sell_market(options['market'], float(options['quantity']))
        elif(usercommand[0] == "Buy_limit"):
            response = trader_class.buy_limit(options['market'], float(options['quantity']), options['rate'])
        elif(usercommand[0] == "Sell_limit"):
            response = trader_class.sell_limit(options['market'], float(options['quantity']), options['rate'])
        elif(usercommand[0] == "Get_open_trades"):
            response = trader_class.get_open_trades(options['market'])
        elif(usercommand[0] == "Cancel_order"):
            response = trader_class.cancel_order(options['market'], options['orderID'])
        elif(usercommand[0] == "Get_balance"):
            if 'market' in options:
                response = trader_class.get_balance(options['market'])
            else:
                response = trader_class.get_balance()
        elif(usercommand[0] == "Get_market_price"):
            response = trader_class.get_market_price(options['market'])
        elif(usercommand[0] == "Sell_OCO_order"):
            response = trader_class.sell_OCO_order(options['market'], float(options['quantity']), options['takeProfitPrice'], options['stopLimit'], options['stopLossPrice'])
        elif(usercommand[0] == "Trade"):
            response = trader_class.trade(options['market'], float(options['quantity']), options['takeProfitPrice'], options['stopLossPrice'])
        elif(usercommand[0] == "Trade_pct"):
            response = trader_class.trade_pct(options['market'], float(options['quantity']), options['takeProfitPct'], options['stopLossPct'])
        
        if response:
            chunk_size=4000
            if len(response)>chunk_size:
                response = [ response[i:i+chunk_size] for i in range(0, len(response), chunk_size) ]
                for message in response:
                    bot.sendMessage(text=str(message), chat_id=adminCID)
            else:
                bot.sendMessage(text=str(response), chat_id=adminCID)
    except Exception as e:
        bot.sendMessage(text=str(e), chat_id=adminCID)


### This function ping 8.8.8.8 and send you result
def ping8(bot, update):
    if not isAdmin(bot, update):
        return
    cmdOut = str(
        subprocess.check_output(
            "ping", "8.8.8.8 -c4", stderr=subprocess.STDOUT, shell=True
        ),
        "utf-8",
    )
    bot.sendMessage(text=cmdOut, chat_id=adminCID)


def startCMD(bot, update):
    if not isAdmin(bot, update):
        return
    bot.sendMessage(
        text="Welcome to Binance Trader bot, Please use /help and read carefully!!",
        chat_id=adminCID,
    )


def helpCMD(bot, update):
    if not isAdmin(bot, update):
        return
    bot.sendMessage(
        text=helpMessage,
        chat_id=adminCID,
    )

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def isAdmin(bot, update):
    print(update)
    chat_id = update.message.chat_id
    if str(chat_id) == adminCID:
        return True
    else:
        update.message.reply_text(
            "You cannot use this bot, because you are not Admin!!!!"
        )
        alertMessage = """Some one tried to use this bot with this information:\n chat_id is {} and username is {} """.format(
            update.message.chat_id, update.message.from_user.username
        )
        bot.sendMessage(text=alertMessage, chat_id=adminCID)
        return False


def main():
    updater = Updater(config.telegram_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", startCMD))
    dp.add_handler(CommandHandler("ping8", ping8))
    dp.add_handler(CommandHandler("help", helpCMD))
    dp.add_handler(MessageHandler(Filters.text, runCMD))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()