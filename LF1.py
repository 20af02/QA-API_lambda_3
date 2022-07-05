import json
from variables import *
import boto3
from requests_aws4auth import AWS4Auth
import requests
from boto3.dynamodb.conditions import Key
from collections import OrderedDict


def parse_elastic_response(response):
    tmp = list()
    for hit in response['hits']['hits']:
        tmp.append(hit['_source']['id'])
    return tmp


def lambda_handler(event, context):
    host = 'https://search-post1-kcl6ksh2qggcjszkz3m7rmqilq.us-east-1.es.amazonaws.com/'
    path = 'posts/_search'
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.session.Session(aws_access_key_id=ACCESS_KEY,
                                        aws_secret_access_key=SECRET_KEY, region_name=region).get_credentials()
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region,
                       service, credentials.token)

    url = host+path
    headers = {'Content-Type': "application/json",
               'Accept': "application/json"}
    AWS_ACCESS_KEY_ID = ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = SECRET_KEY
    print(event)
    try:
        payload = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "tags": event["queryStringParameters"]["q"]
                            }
                        }
                    ]
                }
            }
        }
        r = requests.get(url, auth=(USER, PASS), headers=headers, json=payload)
        print(r.content)
        print("Request Generated Successfully")
    except Exception as e:
        print("Error generating Request:")
        print(e)
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': e

        }

    # DynamoDB for text
    results = json.loads(r.content)
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                                  aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        table = dynamodb.Table('posts')
        ids = parse_elastic_response(results)
        if ids == []:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': "no answers found for this category"

            }
        responses = list()
        ES_URL = ''
        for id in ids:
            resp = table.query(KeyConditionExpression=Key('id').eq(str(id)), )
            responses.append(resp)
        dict = OrderedDict()
        for data in responses:
            dict[data['Items'][0]['id']] = [data['Items']
                                            [0]['date'], data['Items'][0]['posts']]
        print(dict)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(dict)
        }
    except Exception as e:
        print("Error generating Request:")
        print(e)
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': e

        }
