import asyncio
import requests
from fake_useragent import UserAgent
from smsactivate.api import SMSActivateAPI
from tgbot.services.api_sqlite import add_tokenx, delete_temp_token
from tgbot.data.config import API_KEY
import json
from tgbot.data.config import API_KEY_ONLINE_SIM

sa = SMSActivateAPI(API_KEY)
sa.debug_mode = False

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
        await asyncio.sleep(0.1)
        if data['responce'] == 'WARNING_LOW_BALANCE':
            return None
        else:
            await buy_num(code)


async def get_code_onlinesim(tzid, num):
    URL = F'https://onlinesim.ru/api/getState.php'
    PARAMETERS['tzid']=int(tzid)
    PARAMETERS['message_to_code']=1
    i = 0
    while True:
        try:
            data = json.loads(requests.post(url=URL,data=PARAMETERS).text)
            print(data)
            code = data[0]['msg']
            return code
        except Exception as e:
            i+=1
            if i > 5:
                return False
            await asyncio.sleep(15)

async def onlinesim_get_num():
	code = input('Введите номер страны')
	number,transaction_id = await buy_num(code)
	code_msg = await get_code(transaction_id)

async def get_num():
    while True:
        number = sa.getNumberV2(service='cb', country=63)
        try:
            return(number['activationId'],number['phoneNumber'])
        except Exception as e:
            await asyncio.sleep(3)
            print(e)
    

async def get_code(task_id,num):
    while True:
        status = sa.getStatus(id=task_id)
        await asyncio.sleep(15)
        try:
            print(sa.activationStatus(status))
            if sa.activationStatus(status)['status'] != 'STATUS_WAIT_CODE' and sa.activationStatus(status)['status'] != 'Waiting for sms':
                print(sa.activationStatus(status))
                return sa.activationStatus(status)['status']
            if sa.activationStatus(status)['status'] == 'STATUS_CANCEL':
                break
        except:
            await asyncio.sleep(15)
            if status['message'] == 'Current activation canceled and no longer available':
                break
        

async def send_num(online_sim=None):
    if online_sim:
        try:
            user_agent = UserAgent().random
            await asyncio.sleep(0.1)
            link = 'https://deti.bazos.cz/pridat-inzerat.php'
            headers = {
                'Cookie': 'rekkkb=ano; testcookie=ano; testcookieaaa=ano',
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'host': 'deti.bazos.cz',
                'Content-Length': '48',
            }
            await asyncio.sleep(0.1)
            num,task_id = await buy_num(online_sim)
            num = str(num).replace('+','')
            await asyncio.sleep(0.1)
            send_sms_data = f'podminky=1&teloverit=%2B{num}&Submit=Odeslat'
            respnonce = requests.post(url=link, headers=headers,data=send_sms_data)
            if 'Zablokované telefonní číslo' not in respnonce.text:
                i = 0
                while True:
                    await asyncio.sleep(0.1)
                    try:
                        i+=1
                        cookie = respnonce.cookies
                        await asyncio.sleep(0.1)
                        code = await get_code_onlinesim(task_id,num)
                        if code:
                            code = str(code).replace(' ','').replace('\n','')
                            send_code_data = f'klic={code}&klictelefon=%2B{num}&Submit=Odeslat'
                            respnonce = requests.post(url=link, headers=headers,data=send_code_data, cookies=cookie)
                            print(respnonce.cookies)
                            token = str(respnonce.cookies)
                            bid = str(respnonce.cookies)
                            bid = token.split('<Cookie bid=')[1].split(' ')[0]
                            token = token.split('<Cookie bkod=')[1].split(' ')[0]
                            add_tokenx(token,bid)
                            print(respnonce.cookies)
                            return token
                        else:
                            return 'СМС не пришла :('
                    except Exception as e:
                        if i > 5:
                            return 'СМС не пришла :('
                        await asyncio.sleep(60)
                        respnonce = requests.post(url=link, headers=headers,data=send_sms_data)
                        await asyncio.sleep(60)
            else:
                delete_temp_token()
                return 'Номер заблокирован'
        except Exception as e:
            await asyncio.sleep(3)
            print(e)
    else:
        user_agent = UserAgent().random
        await asyncio.sleep(0.1)
        link = 'https://deti.bazos.cz/pridat-inzerat.php'
        headers = {
            'Cookie': 'rekkkb=ano; testcookie=ano; testcookieaaa=ano',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'host': 'deti.bazos.cz',
            'Content-Length': '48',
        }
        await asyncio.sleep(0.1)
        task_id, num = await get_num()
        await asyncio.sleep(0.1)
        send_sms_data = f'podminky=1&teloverit={num}&Submit=Odeslat'
        respnonce = requests.post(url=link, headers=headers,data=send_sms_data)
        print(respnonce.text)
        if 'Zablokované telefonní číslo' not in respnonce.text:
            cookie = respnonce.cookies
            await asyncio.sleep(0.1)
            code = await get_code(task_id=task_id,num=num)
            send_code_data = f'klic={code}&klictelefon=%2B{num}&Submit=Odeslat'
            respnonce = requests.post(url=link, headers=headers,data=send_code_data, cookies=cookie)
            print(respnonce.cookies)
            token = str(respnonce.cookies)
            bid = str(respnonce.cookies)
            bid = token.split('<Cookie bid=')[1].split(' ')[0]
            token = token.split('<Cookie bkod=')[1].split(' ')[0]
            add_tokenx(token,bid)
            print(respnonce.cookies)
            return token
        else:
            delete_temp_token()