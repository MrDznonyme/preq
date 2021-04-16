from selenium import webdriver
import time
from binance.client import Client
from playsound import playsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import string
import pyscreeze
from pynput import mouse
mc = mouse.Controller()
mb = mouse.Button
bl = mb.left
pb = 'IZZHhiZ3SxR0G0N9Ws9PJ64BbNYOo7DtKXEY7hGgjD6SVkTZVI09RqDM1ffPe47e'
prv = 'r5kmbeoGhYjlTHDXldPMxNmU4wOouCmYfpfqRrXjuIXvFEOIqibFnDD1VTWhswNH'
url = 'https://api.binance.com/api/v1/ticker/24hr'
client = Client(pb, prv)


def tm(s):
    time.sleep(s)


def click_photoS(photo, button, timesleep):
    position = pyscreeze.center(pyscreeze.locateOnScreen(photo, grayscale=True, confidence=0.8))
    mc.position = position
    tm(timesleep)
    mc.click(button)


def lbuy(price, quantity):
    buy = client.order_limit_buy(timeInForce='GTC',
                           symbol='XRPUSDT',
                           quantity=quantity,
                           price=str(price),
                           recvWindow=59999)


def lsell(price, quantity):
    client.order_limit_sell(timeInForce='GTC',
                            symbol='XRPUSDT',
                            quantity=quantity,
                            price=str(price),
                            recvWindow=59999)


def rnd(number, n):
    a = str(number).split('.')[0] + '.' + str(number).split('.')[1][0:n]
    return float(a)


def b_amount(usdt ,price):
    am = (usdt / float(price))
    return rnd(am, 2)


def s_amount():
    cryp_balance = float(client.get_asset_balance('XRP')['free'])
    return rnd(cryp_balance, 2)


def dec(t: str):
    letters = string.ascii_lowercase
    f = ''
    for i in t:
        if i.isdigit():
            f += i
            continue
        if i == ':':
            f += '@'
            continue
        if i == '_':
            f += '.'
            continue
        if i == '.':
            f += '.'
            continue
        cpt = 0
        for j in letters:
            if j == i:
                if i != 'a':
                    n = letters[cpt - 1]
                else:
                    n = letters[-1]
                f += n
            cpt += 1
    return str(f)

def sendmail(msga):
    ga = 'qfsgfdu.tbmbn12:hnbjm_dpn'
    gp = 'ghpozgbwlhexpjnd'
    msg = MIMEMultipart()
    msg['From'] = dec(ga)
    msg['To'] = dec(ga)
    msg['Subject'] = "Binance Notification"
    body = msga
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(dec(ga), gp)
    text = msg.as_string()
    server.sendmail(dec(ga), dec(ga), text)
    server.quit()


def chart_check():
    global pre_dif
    html = browser.page_source
    dif = float(html.split('MACD[3]Series')[1].split('">')[1].split('</span>')[0])
    #current = float(html.split('<title data-shuvi-head="true">')[1].split(' |')[0])
    #chart1 = float(html.split('MACD[1]Series')[1].split('">')[1].split('</span>')[0])
    #chart2 = float(html.split('MACD[2]Series')[1].split('">')[1].split('</span>')[0])
    if dif != pre_dif:
        print(dif)##
    if pre_dif != 's':
        if (dif >= 0) and (pre_dif < 0):
            tr = client.get_my_trades(symbol='XRPUSDT', recvWindow=59999)
            if not tr[-1]['isBuyer']:
                print('buying')
                #buy
                try:
                    usdt_balance = float(client.get_asset_balance('USDT')['free'])
                    candles = client.get_historical_klines(symbol='XRPUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,
                        start_str='5 minute ago UTC')
                    current = float(candles[-1][4])
                    buy_order = client.order_market_buy(
                        symbol='XRPUSDT',
                        quoteOrderQty=usdt_balance)
                    tr = client.get_my_trades(symbol='XRPUSDT', recvWindow=59999)
                    b_price = float(tr[-1]['price'])
                    b_qty = float(tr[-1]['qty'])
                    if tr[-1]['isBuyer']:
                        print('Buy Price = ', b_price)
                        playsound('Angry Bird.mp3')
                        if tr[-1]['commissionAsset'] == 'USDT':
                            com = float(tr[-1]['commission'])
                        else:
                            asset = tr[-1]['commissionAsset'] + 'USDT'
                            cc = client.get_historical_klines(symbol=asset,
                                                              interval=Client.KLINE_INTERVAL_30MINUTE,
                                                              start_str='1 hour ago UTC')
                            asset_price = float(cc[-1][4])
                            com = asset_price * float(tr[-1]['commission'])
                        print('Commission = ', com, ' USDT')
                        sendmail('Buy Price = ' + str(b_price) + 'Qty = ' + str(b_qty) + '\nCommission = ' + str(com) + ' USDT' +
                            '\nTotal = ' + str(tr[-1]['quoteQty']))
                except Exception as be:
                        print('Buy Error :> ', be)
        #sell
        elif ((dif <= 0) and (pre_dif > 0)) or (dif < pre_dif):
            tr = client.get_my_trades(symbol='XRPUSDT', recvWindow=59999)
            if tr[-1]['isBuyer']:
                print('Selling')
                try:
                    candles = client.get_historical_klines(symbol='XRPUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,
                        start_str='5 minute ago UTC')
                    current = float(candles[-1][4])
                    b_qty = float(tr[-1]['qty'])
                    if tr[-1]['commissionAsset'] == 'USDT':
                        com = float(tr[-1]['commission'])
                    else:
                        asset = tr[-1]['commissionAsset'] + 'USDT'
                        cc = client.get_historical_klines(symbol=asset,
                            interval=Client.KLINE_INTERVAL_30MINUTE,
                            start_str='1 hour ago UTC')
                        asset_price = float(cc[-1][4])
                        com = asset_price * float(tr[-1]['commission'])
                    wnt = float(tr[-1]['quoteQty']) + 0.7 + (2 * com)
                    print(wnt)
                    if (current * b_qty) > wnt:
                        print("1++++")
                        sell_order = client.order_market_sell(
                            symbol='XRPUSDT',
                            quantity=b_qty
                        )
                        tr = client.get_my_trades(symbol='XRPUSDT', recvWindow=59999)
                        if tr[-1]['isMaker']:
                            playsound('Angry Bird.mp3')
                            print('Total = ', tr[-1]['quoteQty'])
                            s_price = float(tr[-1]['price'])
                            s_qty = float(tr[-1]['qty'])
                            sendmail('Sell Price = ' + str(s_price) + 'Qty = ' + str(s_qty) + '\nTotal = ' + str(tr[-1]['quoteQty']))
                    elif ((dif <= 0) and (pre_dif > 0)) and ((current * b_qty) > (wnt - 0.7)):
                        print("2+++")
                        sell_order = client.order_market_sell(
                            symbol='XRPUSDT',
                            quantity=b_qty
                        )
                        tr = client.get_my_trades(symbol='XRPUSDT', recvWindow=59999)
                        if tr[-1]['isMaker']:
                            playsound('Angry Bird.mp3')
                            print('Total = ', tr[-1]['quoteQty'])
                            s_price = float(tr[-1]['price'])
                            s_qty = float(tr[-1]['qty'])
                            sendmail('Sell Price = ' + str(s_price) + 'Qty = ' + str(s_qty) + '\nTotal = ' + str(tr[-1]['quoteQty']))
                except Exception as bs:
                        print('Sell Error :> ', bs)
    pre_dif = dif


driver_path = "chromedriver.exe"
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
option = webdriver.ChromeOptions()
option.binary_location = brave_path
browser = webdriver.Chrome(executable_path=driver_path, options=option)
browser.get("https://www.binance.com/en/trade/XRP_USDT?layout=basic")
#tm(1)
#click_photoS('Settings.png', bl, 1)
#tm(1)
#click_photoS('MD.png', bl, 1)

# 0: Open time
# 1: Open
# 2: High
# 3: Low
# 4: Close
# 5: Volume
# 6: Close time
# 7: Quote asset volume
# 8: Number of trades
# 9: Taker buy base asset volume
# 10: Taker buy quote asset volume
# 11: Can be ignored
# MACD[3]Series   rgb(3, 166, 109);">  </span>

pre_dif = 's'
print('Start')
while True:
    try:
        chart_check()
    except Exception as ge:
        print('General Error : ', ge)
    tm(0.01)
