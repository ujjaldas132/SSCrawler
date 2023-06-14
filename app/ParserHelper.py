'''
author: Ujjal Das
github: ujjaldas132
date: June, 2023
<p>

'''


import json

from modelClass import Action, Prefix, ServiceEncoder, Resource, Condition
import re

def get_condition_table(table):
    conditionKey_list = []
    rows = table.find_all('tr')
    num_rows = len(rows)
    for i in range(1, num_rows):
        row = rows[i]

        columns = row.find_all('td')
        if (len(columns[0].findAll('a')) == 2):
            cKey = re.split('<|>', str(columns[0].findAll('a')[1]))[2]
        else:
            cKey = columns[0].text.strip()

        description = columns[1].text.strip()
        cType = columns[2].text.strip()

        condition = Condition()
        condition.conditionKey = cKey
        condition.type = cType
        condition.desc = description
        conditionKey_list.append(condition)
    return conditionKey_list


def get_resource_table(table):
    resources_list = []
    rows = table.find_all('tr')
    num_rows = len(rows)
    for i in range(1, num_rows):

        row = rows[i]
        columns = row.find_all('td')

        if(len(columns[0].findAll('a'))==2):
            rType = re.split('<|>', str(columns[0].findAll('a')[1]))[2]
        else:
            rType = columns[0].text.strip()

        arn = columns[1].find('code').text

        conditionKeys = columns[2].text
        resourceObject = Resource()
        resourceObject.resourceType = rType
        resourceObject.arn = arn
        resourceObject.conditionKey = conditionKeys
        resources_list.append(resourceObject)
    return resources_list


def get_action_table(table) :
    action_list = []
    rows = table.find_all('tr')
    num_rows = len(rows)
    for i in range(1, num_rows):
        row = rows[i]
        columns = row.find_all('td')
        num_cols = len(columns)
        action = columns[0].findAll('a')
        if action == None or num_cols!=6:
            n = len(action_list)
            resourceTypes = columns[1].findAll('p')
            for resourceType in resourceTypes:
                action_list[n - 1].resources.append(str(resourceType.text.strip()))
            condition_key = columns[1].findAll('p')
            for key in condition_key:
                action_list[n - 1].conditionKey.append(str(key.text.strip()))
            continue
        else:
            if (action[0].get('id')!=None):
                action = re.split('-', action[0]['id'])[1]
            else:
                action = action[0]['href']

        description = columns[1].text.strip()

        access = columns[2].text.strip()

        if (num_cols > 3):
            resources = columns[3].findAll('p')

        if num_cols > 4:
            condition_key = columns[4].findAll('p')

        if num_cols > 5:
            dependent_action = columns[5].text.strip().split(",")

        action_obj = Action()
        action_obj.action = str(action)
        action_obj.access = str(access)
        action_obj.description = str(description.strip())
        if num_cols > 3:
            for resource in resources:
                action_obj.resources.append(str(resource.text.strip()))
        if num_cols > 4:
            for key in condition_key:
                action_obj.conditionKey.append(str(key))
        if num_cols > 5:
            for da in dependent_action:
                if(str(da)!=""):
                    action_obj.dependentActions.append(str(da))

        action_list.append(action_obj)
    return action_list