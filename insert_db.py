import boto3
from variables import *
import json
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                          aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
table = dynamodb.Table('posts')

with open('DynamoDB.json', 'r', encoding='utf-8') as f:
    rows = json.loads("[" +
                      f.read().replace("}\n{", "},\n{") +
                      "]")


x = 0
y = rows.__len__()


with table.batch_writer() as batch:
    for row in rows:
        batch.put_item(Item=row)
        x += 1
        print(x)
        if x % 100 == 0:
            time.sleep(10)
        if x % 999 == 0:
            time.sleep(100)
