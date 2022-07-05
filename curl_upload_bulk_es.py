from variables import *
from requests_aws4auth import AWS4Auth
import boto3
import requests
import json

host = '<ES_URL>'
path = '<ES_INDEX>/_doc/1/'
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region, service,
                   session_token=credentials.token)

url = host + path



r = requests.post(url, auth=("Demo-ES1", "Demo-ES1"), json=payload)
print(r.text)
