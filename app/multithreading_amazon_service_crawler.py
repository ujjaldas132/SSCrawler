'''
author: Ujjal Das
github: ujjaldas132
date: June, 2023
<p>

'''
import concurrent.futures
from amazon_service_crawler import get_prefix_json
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import threading
from multiprocessing.pool import Pool


if __name__ == '__main__':
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=40)
    url = "https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    services_block = soup.findAll('div', {'class': 'highlights'})
    services = services_block[0].find_all('li')
    for service in services:
        pool.map(get_prefix_json, service.find_all('a'))
    pool.shutdown(wait=True)
    print("Finished...!")

    #todo lookup the GIL(global interpreter lock)
    '''
    Explain why current code doesnt result in speedup
    fix the code ---> done
    bonus : read about co-routine
    '''