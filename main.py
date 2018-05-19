import os
import schedule
import time
import requests
import json

import fire

COINMARKETCAP_API_URL = "https://api.coinmarketcap.com/v2/ticker/?limit=10"
COINMARKETCAP_API_URL_SINGLE_COIN = "https://api.coinmarketcap.com/v2/ticker/"


def notify(title="💰", subtitle="", message="", icon=None, url=None):
    message = 'terminal-notifier -title "%s" -subtitle "%s" -message "%s" -sound default' % (title, subtitle, message)
    if icon: message += " -appIcon %s" % icon
    if url: message += " -open '%s'" % url
    os.system(message)


def generate_coins_config():
    """
    Writes the basic config for the top 10 currencies from CoinMarketCap to config.json
    Sets a min and max at 20% difference from when the script was run
    """
    url = COINMARKETCAP_API_URL
    r = requests.get(url)
    data = r.json()['data']

    coin_list = []
    for coin_id in data:
        coin_data = data[coin_id]
        coin_list.append({
            "coinmarketcap_id": coin_id,
            "name": coin_data["name"],
            "image": "https://s2.coinmarketcap.com/static/img/coins/32x32/%s.png" % coin_id,
            "website_url": "https://coinmarketcap.com/currencies/%s/" % coin_data["website_slug"],
            "symbol": coin_data["symbol"],
            "active": True,
            "max": coin_data['quotes']['USD']['price'] * 1.2,
            "min": coin_data['quotes']['USD']['price'] * 0.8
        })

    with open('coin-config.json', 'w') as outfile:
        json.dump(coin_list, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    message = "\n".join(["%s: %s" % (c['symbol'], c['name']) for c in coin_list])
    print("Generated coin-config.json for the following coins:\n\n" + message + "\n")


def get_coin_current_price(coin_id):
    r = requests.get(COINMARKETCAP_API_URL_SINGLE_COIN + coin_id)
    return r.json()['data']['quotes']['USD']['price']


def compare_prices():
    config = None

    with open("coin-config.json") as file:
        config = json.load(file)

    for coin in config:
        if coin['active']:
            coin_current_price = get_coin_current_price(coin['coinmarketcap_id'])
            if coin_current_price > coin['max'] or coin_current_price < coin['min']:
                notify(
                    title="%s Alert" % coin['name'],
                    subtitle="Value: %sUSD" % coin_current_price,
                    message="Click here to view",
                    icon=coin['image'],
                    url=coin['website_url']
                )
                print("%s: %sUSD" % (coin['symbol'], coin_current_price))


def track_coins():
    notify(subtitle="Watching coins")
    schedule.every().minute.do(compare_prices)

    print("Initiated Coin Price tracker")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    fire.Fire({
      'track_coins': track_coins,
      'generate_coins_config': generate_coins_config,
    })
