import requests
import asyncio
import json
import time

from tgbot.data.config import API_KEY_ONLINE_SIM


PARAMETERS = {
	'lang':'ru',
	'apikey':API_KEY_ONLINE_SIM,
}

async def get_balance_online_sim():
	URL = F'https://onlinesim.ru/api/getBalance.php'
	data = json.loads(requests.post(url=URL,data=PARAMETERS).text)
	return data['balance']


async def get_statistics_online_sim():
	country_codes = [49,48,420]
	responce = []

	URL = F'https://onlinesim.ru/api/getNumbersStats.php'
	for code in country_codes:
		PARAMETERS['country']=code
		data = json.loads(requests.post(url=URL,data=PARAMETERS).text)
		price = data['services']['service_bazos']['price']
		count = data['services']['service_bazos']['count']
		responce.append({'country':code,'price':price,'count':count})
	return responce

async def buy_num(code):
	while True:
		try:
			URL = F'https://onlinesim.ru/api/getNum.php'
			PARAMETERS['country']=str(code)
			PARAMETERS['service']='Bazos'
			PARAMETERS['number']=True
			data = json.loads(requests.post(url=URL,data=PARAMETERS).text)
			number = data['number']
			transaction_id = data['tzid']
			return number,transaction_id
		except Exception as e:
			print(e)
			await asyncio.sleep(3)

async def get_code(tzid):
	URL = F'https://onlinesim.ru/api/getState.php'
	PARAMETERS['tzid']=int(tzid)
	PARAMETERS['message_to_code']=1
	while True:
		try:
			data = json.loads(requests.post(url=URL,data=PARAMETERS).text)
			print(data)
			code = data[0]['msg']
			return code
		except Exception as e:
			await asyncio.sleep(15)

async def onlinesim_get_num():
	code = input('Введите номер страны')
	number,transaction_id = await buy_num(code)
	code_msg = await get_code(transaction_id)
	print(code_msg)


if __name__ == '__main__':
	asyncio.run(onlinesim_get_num())