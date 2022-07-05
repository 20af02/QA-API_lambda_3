import pandas as pd
from collections import OrderedDict
import csv
import json
import collections
import unicodedata
orderedDict = collections.OrderedDict()


def get_tags(string):
    tags = string.replace("\"", '').replace(
        '\'', '').replace('[', '').replace(']', '').split(',')

    return tags


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    x = OrderedDict([("id", {})])
    jsonString = json.dumps(x)
    all_data = []
    with open(csvFilePath) as csvf:
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.reader(csvf)
            for row in csvReader:
                if row[0] == 'id':
                    continue

                tmp = str(row[2:])
                tmp = tmp.strip()

                if row[0] == '404026':
                    print(tmp)
                    print(all_data)

                tmp2 = json.dumps(tmp)

                y = "{{\"id\": \"{}\", \"date\": \"{}\", \"posts\": {} }}".format(
                    row[0], row[1], tmp2)
                jsonf.write(y)

#
                jsonf.write("\n")
            jsonf.write("\n")


csvFilePath = r'DynamoDB.CSV'
jsonFilePath = r'DynamoDB.json'
csv_to_json(csvFilePath, jsonFilePath)
