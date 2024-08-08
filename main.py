from InquirerPy.inquirer import select
from util import clear_terminal, scrape
import time

clear_terminal()

main_menu_choices = ['Scrape Proxies', 'Check Proxies', 'Proxy Count', 'Export', 'Exit']
proxy_menu_choices = ['All', 'Http', 'Https', 'Socks4', 'Socks5']
anonymity_menu_choices = ['All', 'Transparent (Personal IP Can Still Be Retrieved)', 'Anonymous (Personal IP Doesnt Make It Through But The Service Can See Its A Proxy)', 'Elite (Personal IP Doesnt Make It Through And The Service Cannot Tell You\'re Using A Proxy)']

menu_selection = select(
    instruction='(Use The Arrow Keys To Navigate And Enter To Pick An Option!)',
    message='Welcome To The Proxy Checker/Scraper. Choose An Option Below To Continue!',
    choices=main_menu_choices,
    default=main_menu_choices[0],
    qmark=''
)

menu_selection.execute()

if menu_selection.result_name == main_menu_choices[0]:

    proxy_type = select(
        message='Choose a proxy type:',
        choices=proxy_menu_choices,
        default=proxy_menu_choices[0],
        qmark=''
    )
    proxy_type.execute()

    anonymity = select(
        message='Choose an anonymity:',
        choices=anonymity_menu_choices,
        default=anonymity_menu_choices[0],
        qmark=''
    )
    anonymity.execute()

    print()
    print('Starting Scrape!\n')

    start = time.time()

    count = scrape(protocol=proxy_type.result_name.lower(), anonymity=anonymity.result_name.lower())

    finish = time.time() - start

    print(f'Finished Scraping {count} Proxies In {"%.3f" % finish} Seconds!')
    
if menu_selection.result_name == main_menu_choices[1]:
    clear_terminal()
if menu_selection.result_name == main_menu_choices[2]:
    clear_terminal()
if menu_selection.result_name == main_menu_choices[3]:
    clear_terminal()
if menu_selection.result_name == main_menu_choices[4]:
    clear_terminal()
    exit()