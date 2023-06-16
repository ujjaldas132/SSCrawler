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

        arn = columns[1].find('code').text.strip()

        conditionKeys = columns[2].text.strip()
        resourceObject = Resource()
        resourceObject.resourceType = rType
        resourceObject.arn = arn
        if len(conditionKeys) > 0:
            for conditionKey in conditionKeys.split("\n"):
                resourceObject.conditionKey.append(conditionKey.strip())
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
        access= ""
        description = ""
        if action == None or num_cols!=6:
            # todo dont have to merge -> done
            action = action_list[-1].action
            description = action_list[-1].description
            access = action_list[-1].access
            columns = ["dump"]+columns
            columns = ["dump"]+columns
            columns = ["dump"]+columns
        else:
            if (action[0].get('id')!=None):
                action = re.split('-', action[0]['id'])[1]
            else:
                action = action[0]['href']

            description = columns[1].text.strip()
            access = columns[2].text.strip()

        resources = columns[3].findAll('p')
        condition_key = columns[4].findAll('p')
        dependent_action = columns[5].text.strip().split(",")

        action_obj = Action()
        action_obj.action = str(action)
        action_obj.access = str(access)
        action_obj.description = str(description.strip())

        for resource in resources:
            action_obj.resources.append(str(resource.text.strip()))

        for key in condition_key:
            action_obj.conditionKey.append(str(key.text.strip()))

        for daction in dependent_action:
            if(str(daction)==""):
                continue
            for da in daction.split("\n"):
                if str(daction)!="":
                    action_obj.dependentActions.append(str(da.strip()))

        action_list.append(action_obj)
    return action_list