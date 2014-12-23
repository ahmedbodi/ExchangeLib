import time
from bittrex import Bittrex

class BittrexWrapper(object):

    def __init__(self, apiKey, apiSecret):
	self.apiKey = apiKey
	self.apiSecret = apiSecret
	self.api = Bittrex(self.apiKey, self.apiSecret)
	self.failure = (False, 0, 0)

    def get_price(self, market_code, base_code='BTC'):
	self.currency_code = '%s-%s' % (base_code, market_code)
	price_ticker = bittrex_api.get_ticker(currency_code)
	if price_ticker['success']:
		return price_ticker
	else:
		return {}

    def get_address(self):
        deposit_address_query = self.api.get_deposit_address(base_code)
        if deposit_address_query['success'] == False and deposit_address_query['message'] == 'ADDRESS_GENERATING':
                time.sleep(10)
                deposit_address_query = self.api.get_deposit_address(base_code)

    def buy_coins(self, market_code, price, base_code='BTC'):
	currency_code = '%s-%s' % (base_code, market_code)

	price_ticker = self.api.get_ticker(currency_code)
	if price_ticker['success']:
		ask_price = price_ticker['result']['Ask']
	else:
		return self.failure

	quantity = price / ask_price 
	sell_market_query = self.api.buy_limit(currency_code, quantity, ask_price)
	if sell_market_query['success']:
		order_uuid = sell_market_query['result']['uuid']
	elif not sell_market_query['success']:
		return self.Failure

	# Sleep for long enough for bittrex to process the order
	time.sleep(30)  # 4) Check the Order
	order_status_query = bittrex_api.get_order(order_uuid)
	if order_status_query['success']:
		aOrder = dict()
		aOrder['price'] = order_status_query['result']['Price']
		aOrder['Quantity'] = order_status_query['result']['Quantity']
		aOrder['Exchange'] = order_status_query['result']['Exchange']
		aOrder['completed'] = True
		return aOrder['completed'], aOrder['price'], aOrder['Quantity']
	else:
		return self.Failure

