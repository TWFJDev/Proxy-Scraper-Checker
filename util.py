import requests
import models
import platform
import os
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=models.engine)
session = Session()

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

def get_all_proxies(protocol, anonymity):
    proxies = []

    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get'

    params = {
        'request': 'displayproxies',
        'protocol': protocol,
        'proxy_format': 'ipport',
        'anonymity': anonymity,
        'format': 'json'
    }

    resp = requests.get(url, params=params)

    info = resp.json()

    for proxy in info['proxies']:
        proxies.append(proxy['proxy'])

    return proxies

def add_proxies_to_db(protocol, anonymity):
    proxies = get_all_proxies(protocol, anonymity)

    db_proxies = []

    data_check = session.query(models.Proxies).all()

    for db_proxy in data_check:
        db_proxies.append(f'{db_proxy.ip_address}:{db_proxy.port}')

    for proxy in proxies:
        if proxy not in db_proxies:
            data = models.Proxies(ip_address=proxy.split(':')[0], port=proxy.split(':')[1], http=None, https=None, socks4=None, socks5=None, ssl=None, country=None, anonymity=None, status=None, last_checked=None)
            session.add(data)
            session.commit()
            session.close()

    return session.query(models.Proxies).count()

def scrape(protocol, anonymity):
    return add_proxies_to_db(protocol, anonymity)

def check(timeout: int, proxy: str, id):
    ssl = None
    anony = None

    url = 'http://httpbin.org/get'

    protocols = ['http', 'https', 'socks4', 'socks5']

    for proto in protocols:
        proxies = {'http': f'{proto}://{proxy.split(":")[0]}:{proxy.split(":")[1]}', 'https': f'{proto}://{proxy.split(":")[0]}:{proxy.split(":")[1]}'}

        try:
            resp = requests.get(url, proxies=proxies, timeout=timeout)

            if resp.status_code == 200:
                https_url_check = 'https://httpbin.org/get'

                https_resp = requests.get(url, proxies=proxies, timeout=timeout)

                ip_url = f'http://ip-api.com/json/{proxy.split(":")[0]}?fields=message,country,mobile,proxy,hosting,query'

                ip_resp = requests.get(ip_url, proxies=proxies)

                if https_resp.status_code == 200:
                    response = requests.get(url)
                    info = response.json()

                    ssl = 'YES'
                else:
                    ssl = 'NO'

                if ',' in resp.json()['origin']:
                    anony = 'TRANSPARENT'
                elif ip_resp.json()['proxy'] == True:
                    anony = 'ANONYMOUS'
                elif ip_resp.json()['hosting'] == True:
                    anony = 'ANONYMOUS'
                else:
                    anony = 'ELITE'

                print(f'| PROTOCOL: {proto.upper()} | PROXY: {proxy} | STATUS: ALIVE | ANONYMITY: {anony} | SSL: {ssl} | COUNTRY: {ip_resp.json()["country"].upper()} | TIMEOUT: {int(resp.elapsed.microseconds / 1000)} MS |')
                
            else:
                print(f'| PROTOCOL: {proto.upper()} | PROXY: {proxy} | STATUS: DEAD |')
        except:
            print(f'| PROTOCOL: {proto.upper()} | PROXY: {proxy} | STATUS: DEAD |')

# proxies = session.query(models.Proxies).all()

# for proxy in proxies:
#     check(10, f'{proxy.ip_address}:{proxy.port}', proxy.id)