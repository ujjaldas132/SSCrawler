'''
author: Ujjal Das
github: ujjaldas132
date: June, 2023
<p>

'''

import json
from modelClass import Action, Prefix, ServiceEncoder, Resource, Condition
from ParserHelper import *
import requests
import re
import lxml
from bs4 import BeautifulSoup
import time
import random


def get_prefix_json(prefix_service_html) :
    prefixObj = Prefix()
    next_url = "https://docs.aws.amazon.com/service-authorization/latest/reference/" + prefix_service_html['href'].split("./")[1]
    prefixObj.link.append(str(next_url))

    resp = requests.get(next_url)
    soup = BeautifulSoup(resp.content, 'lxml')

    prefix_name = soup.find('code', {'class': 'code'}).text.strip()
    prefixObj.prefix = prefix_name  # todo change prefix-> done

    print(prefix_name, next_url)

    tables = soup.findAll('div', {'class': 'table-contents disable-scroll'})
    action_list = []
    if (len(tables) > 0):
        table = tables[0]
        action_list = get_action_table(table)

    resource_list = []
    condition_list = []
    if (len(tables) > 1):
        resouse_table = tables[1]
        if resouse_table.find_all('th')[0].text.strip() == "Resource types":
            resource_list = get_resource_table(resouse_table)
        else:
            # if resource table is missing
            condition_list = get_condition_table(resouse_table)

    if (len(tables) > 2):
        conditionTable = tables[2]
        condition_list = get_condition_table(conditionTable)

    prefixObj.actions = action_list
    prefixObj.resources = resource_list
    prefixObj.conditions = condition_list

    jsonstr = json.dumps(prefixObj, indent=4, cls=ServiceEncoder)
    with open("output/" + prefix_name + ".json", "w") as outfile:
        outfile.write(jsonstr)
    time.sleep(random.randint(1,10))
    print("finish : ", prefix_name)


if __name__ == '__main__':
    url = "https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    services_block = soup.findAll('div', {'class': 'highlights'})
    services = services_block[0].find_all('li')

    for service in services:
        for prefix_service in service.find_all('a'):
            get_prefix_json(prefix_service)