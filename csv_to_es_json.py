from collections import OrderedDict
import csv
import json
import collections
orderedDict = collections.OrderedDict()


def get_tags(string):
    tags = string.replace("\"", '').replace(
        '\'', '').replace('[', '').replace(']', '').split(',')
    return tags


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    x = OrderedDict([("index", {})])
    jsonString = json.dumps(x)
    print(jsonString)
    with open(csvFilePath) as csvf:
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.reader(csvf)
            for row in csvReader:
                if row[0] == 'id':
                    continue
                y = "{{\"index\":{{\"_index\": \"posts\", \"_id\": \"{}\"}}}}".format(
                    row[0])
                jsonf.write(y)
                jsonf.write("\n")
                tmpstr = ""
                for tmp in row[1:]:
                    tags = get_tags(tmp)
                    for tag in tags:
                        tmpstr += "\"{}\",".format(tag)
                tmpstr = tmpstr[:-1]
                if tmpstr == "[]":
                    tmpstr = ""

                x = "{{\"id\": \"{}\", \"tags\": [{}]}}".format(
                    row[0], tmpstr)

                jsonf.write(x)
                jsonf.write("\n")


csvFilePath = r'DynamoDB.CSV'
jsonFilePath = r'DynamoDB.json'
csv_to_json(csvFilePath, jsonFilePath)
