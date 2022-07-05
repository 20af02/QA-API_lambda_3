import json
from variables import *
import boto3
import datetime
import uuid


def lambda_handler(event, context):
    tmp = json.loads(event["body"])
    id = str(int(uuid.uuid4()))
    date = datetime.datetime.utcnow().isoformat()
    posts = tmp['posts']
    post = {
        "id":  id,
        "date": date,
        "posts": posts
    }

    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                                  aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        table = dynamodb.Table('posts')
    except Exception as e:
        return{
            'statusCode': 503,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Error Posting Accessing DynamoDB." + str(e)
        }

    try:
        with table.batch_writer() as batch:
            batch.put_item(Item=post)
    except Exception as e:
        print(e)
        return{
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "Error Posting Question." + str(e)
        }
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': "Posted Question Successfully."
    }
