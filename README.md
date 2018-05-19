# Coin Price Notifications
Sends desktop notifications about the prices of crypto currencies, when their price is different than a fixed min or max price.


## Requirements:
- Mac OSX
- Python3
- [terminal-notifier](https://github.com/julienXX/terminal-notifier)


## Installation

Clone and access the repository 
```
git clone https://github.com/RyanOM/coinPriceNotifications.git
cd coinPriceNotifications
```

Create a Python3 virtualenv and activate it:
```
virtualenv coinsVirtualEnv -p python3
source coinsVirtualEnv/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

## Instructions


### Inital Config

You can generate listeners for the top ten currencies on [https://coinmarketcap.com](https://coinmarketcap.com/) by running:
```
python main.py generate_coins_config
```

By default, this will generate notifications when the price goes over/under 20% than the current price.
You can specify a different threshold by running the command as such (in the case of 5%):
```
python main.py generate_coins_config 5
```

You can also modify the `coin-config.json` file and adjust the `min` and `max` values.

### Running the notificatins

You can start the listener by running:
```
python main.py track_coins
```

Clicking on the notification will direct you to the [Coinmarketcap](https://coinmarketcap.com/) page of the currency.

## Screenshots:

![alt text](https://github.com/RyanOM/coinPriceNotifications/blob/master/images/example.jpg "Example Bitcoin Notification")

