# Binance-Trader
This is a Simple Binance Trader as a Telegram Bot.<br/>
With TakeProfit and Stoploss Trades using OCO type of trades.<br/>
For TakeProfit and Stoploss you can either use the exact value or you can use percentage.<br/>
You can also get your balance and use the bot for simple market and limit buy and sell orders.<br/>

# How to install and use:
1. To begin, you'll need an Access Token for your telgram bot that you can make using BotFather. then you need your API keys frm binance. be sure to turn withdrawal option off.
 
2. First install some dependencies:
  Best way is use Virtualenv:
  ```bash
  virtualenv -p python3 .env
  source .env/bin/activate
  pip install -r requirements.txt
  ```
 
3. After create your bot and get your Token from botFather, send some text(more than two message) to your bot and use this command to find your chat_id:
  use @userinfobot bot to get your chat_id by sending /start to bot. 
Put your chat_id and Token and Binance's API keys in config.
 
4. Run code:
 ```bash
 python telegramBot.py
 ```
 
5. Send you command via Telegram's Bot

 
## Sample of commands to use:
/start : to start using the bot<br/>
/ping8 : to send ping and check your connection<br/>
/help : to get list of all the possible commands<br/>
<br/>
the rest of the commands:<br/>
Buy_market --market market --quantity quantity<br/>
Sell_market --market market --quantity quantity<br/>
Buy_limit --market market'] --quantity quantity --rate rate<br/>
Sell_limit --market market'] --quantity quantity --rate rate<br/>
Get_open_trades --market market<br/>
Cancel_order --market market --orderID orderID<br/>
Get_balance --symbol symbol<br/>
Get_market_price --market market<br/>
Sell_OCO_order --market market --quantity quantity --takeProfitPrice takeProfitPrice --stopLimit stopLimit --stopLossPrice stopLossPrice<br/>
Trade --market market --quantity quantity --takeProfitPrice takeProfitPrice --stopLossPrice stopLossPrice<br/>
Trade_pct --market market --quantity quantity --takeProfitPct takeProfitPct --stopLossPct stopLossPct<br/>
Transfer_dust --symbol symbol<br/>
<br/>
*you can also use amount of BTC instead of quantity (--amount amount)<br/>
*for get_balance market argument is optional. default value is BTC<br/>
*if you dont use amount or quantity minimum quantity will be used<br/>
<br/>
example:<br/>
Get_balance --market BTC<br/>
Trade --market ETHBTC --quantity 0.005 --takeProfitPrice 0.038 --stopLossPrice 0.036<br/>
Trade_pct --market ETHBTC --quantity 0.005 --takeProfitPct 1.2 --stopLossPct 2<br/>
<br/>
