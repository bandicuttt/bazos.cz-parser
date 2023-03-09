import asyncio
from create_new_tokens import send_num
from tgbot.services.api_sqlite import add_tokenx, delete_temp_token, get_category_filters, get_tokensx, get_tokenx, update_adsx
import requests
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup

url_categories = {
    'kids': 'https://deti.bazos.cz/',
    'electro': 'https://elektro.bazos.cz/',
    'house_and_garden': 'https://dum.bazos.cz/',
    'photo': 'https://foto.bazos.cz/',
    'music': 'https://hudba.bazos.cz/',
    'books': 'https://knihy.bazos.cz/',
    'smartphones': 'https://mobil.bazos.cz/',
    'clothes': 'https://obleceni.bazos.cz/',
    'pc': 'https://pc.bazos.cz/',
    'sport': 'https://sport.bazos.cz/'
}

def get_headers_for_number(category, is_check=None):
    user_agent = UserAgent().random
    host = (url_categories.get(category)).replace('https://','').replace('/','')
    if is_check:
        token = is_check
    else:
        try:
            token = get_tokenx(active=1, temp=0)['token']
        except TypeError:
            return None, None, None
    if token:
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'host': host,
            # 'Cookie': 'bid=59845556; testcookie=ano',
            'cookie': f'rekkk=ano; __gfp_64b=cNMcSnuqq4GxCdlZxigY0TsjehJAp2XMEXpwgcNQWAj.R7|1675635501; __gads=ID=46bc3c64e01567d2-22ed1703a2db00ac:T=1675635556:RT=1675635556:S=ALNI_MYADzNxPoDdwLz6-MyKDkxZfed50Q; __gpi=UID=00000bb0f175f17e:T=1675635556:RT=1675635556:S=ALNI_MbM0kenWqmp8Sxq5nwsDeXc_uve8Q; testcookie=ano; __gsas=ID=dfad3076884da254:T=1675635557:S=ALNI_MY4SIers4sMnOUK7aGpg09DU-LrSA; bid=59845556; bkod={token}'
        }
        link = url_categories.get(category) + 'detailtel.php'
        return link,headers, token

        

def get_headers(category):
    user_agent = UserAgent().random
    host = (url_categories.get(category)).replace('https://','').replace('/','')
    return({
        'User-Agent': user_agent,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'host': host
    })

async def get_all_ads(html_data, category_name):
    ads_list = list()
    soup = BeautifulSoup(html_data, 'lxml')
    for ads in soup.find_all('div', class_='inzeraty inzeratyflex'):
        ads_url = url_categories.get(category_name)[:-1] + ads.find('a',href=True)['href']
        ads_id = ads_url.split('/')[4]
        photo = ads.find('img')['src']
        ads_name = ads.find('img')['alt']
        price = ads.find('div',class_='inzeratycena').get_text().replace(' ','').replace('Kč','')
        views = ads.find('div',class_='inzeratyview').get_text().replace(' ','').replace('x','')
        date = ads.find('span',class_='velikost10').get_text().replace(' - TOP - [','').replace(']','').replace(' ','').replace('-[','')
        is_top = ads.find('span',class_='velikost10').get_text()
        if 'TOP' in is_top:
            is_top = True
        else:
            is_top = False

        ads_list.append({
            'url': ads_url,
            'ads_id': ads_id,
            'photo': photo,
            'ads_name': ads_name,
            'price': price,
            'views': views,
            'date': date,
            'top': is_top,
            'category_name': category_name
        })
        
    return ads_list

async def get_ads_list(page, user_id):
    if user_id != 'check':
        all_categiries = get_category_filters(id=user_id)
        active_categories = [cat for cat in all_categiries if all_categiries[cat] == 1]
        category_name = random.choice(active_categories)
        headers_request = get_headers(category_name)
        url = url_categories.get(category_name) + str(page) + '/'
        html_data = requests.get(url, headers_request).text
        return(await get_all_ads(html_data,category_name), category_name)
    else:
        category_name = 'kids'
        headers_request = get_headers(category_name)
        url = url_categories.get(category_name) + str(page) + '/'
        html_data = requests.get(url, headers_request).text
        return(await get_all_ads(html_data,category_name), category_name)
        

async def get_seller_ads_count(seller_profile_link, category_name):
    headers_request = get_headers(category_name)
    await asyncio.sleep(0.1)
    html_data = requests.get(seller_profile_link, headers_request).text
    await asyncio.sleep(0.1)
    soup = BeautifulSoup(html_data, 'lxml')
    seller_ads_count = soup.find('div',class_='inzeratynadpis').get_text().replace('Všechny inzeráty uživatele (', '').replace('):','')
    return seller_ads_count

async def get_seller_link(ads_url, category_name, ads_id):
    headers_request = get_headers(category_name)
    await asyncio.sleep(0.1)
    html_data = requests.get(ads_url, headers_request).text
    await asyncio.sleep(0.1)
    soup = BeautifulSoup(html_data, 'lxml')
    seller_profile_link = ((soup.find('td',class_='listadvpravo')).find_all('a', href=True)[0])['href']
    idphone = seller_profile_link.split('&')[1].replace('idphone=','')
    update_adsx(ads_id,idphone=idphone)
    return(await get_seller_ads_count(seller_profile_link,category_name),idphone)


def check_ads_count(max_count, count):
    if int(count) <= max_count:
        return True
    else:
        return False

def check_views(max_views,views):
    if int(views) <= max_views:
        return True
    else:
        return False


async def check_token():
    try:
        ads_list,category_name = await get_ads_list(0, 'check')
        for ads in ads_list:
            seller_ads_count,idphone = await get_seller_link(ads['url'], category_name, ads['ads_id'])
            await asyncio.sleep(0.1)
            return ads['ads_id'],idphone
    except Exception as e:
        print(e)

async def check_token_with_get_num(tokens):
    good = 0
    bad = 0
    for token in tokens:
        try:
            if get_tokenx(token=token):
                bad+=1
            else:
                add_tokenx(token,'hand')
                good+=1
                # idphone,ads_id = await check_token()
                # link, headers, token = get_headers_for_number('kids',token)
                # if link:
                #     params = {
                #         'idi': ads_id,
                #         'idphone': idphone
                #     }
                #     html_data = requests.get(url=link, headers=headers, params=params).text
                #     soup = BeautifulSoup(html_data, 'lxml')
                #     number = soup.find('a',href=True).get_text()
                #     if 'max tel' in str(number):
                #         add_tokenx(token,'hand')
                #         good+=1
                #     else:
                #         print(number)
                #         int(number)
                #         add_tokenx(token,'hand')
                #         good+=1
                # else:
                #     bad+=1
        except Exception as e:
            print(1111)
            bad+=1
    return good,bad