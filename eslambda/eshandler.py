import boto3
import json
import requests
import urllib
from requests_aws4auth import AWS4Auth

region = 'us-west-2'
service = 'es'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

ES_HOST  = 'https://<XXX-ES-HOST-NAME-XXX>.us-west-2.es.amazonaws.com/'

def es_search(event):

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).

    es_index = event['resource'].split('/')[-1]
    url =  ES_HOST  + es_index  + '/_search?filter_path=_shards'
    
    #print(event)
    
    if 'size' in event['queryStringParameters']:
        req_size = int(event['queryStringParameters']['size'])
    else:
        req_size = 10
        
    query = {
        "size": req_size,
        "query": {
           "bool": {
             "filter": [
                 {
                     "query_string": {
                          "query": event['queryStringParameters']['q']
                      }
                 }
              ]
            }
        }
    }
        
    data=urllib.parse.urlencode(query)
    headers = { "Content-Type": "application/json" }
    resp = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query), timeout=None)
    return resp


def es_ingest(event):


    es_index = event['resource'].split('/')[-1]
    url = ES_HOST + es_index + '/_bulk?filter_path=items.index._shards'

    # Below code will be used while sending a request  
    headers = { "Content-Type": "application/json" }

    # Bulk index
    data_json = event['body'].split('\n')
    result = []
    bulk_prefix = '{{"index": {{"_index": "{}"}}}}\n'.format(es_index)
    for item in data_json:
        if item:
            result.append(bulk_prefix)
            result.append(item + '\n')
    data = ''.join(result)
    #print(data)
        

    headers = { "Content-Type": "application/json" }
    resp = requests.post(url, auth=awsauth, headers=headers, data=data, timeout=None)
        
    return resp


# Lambda execution starts here
def lambda_handler(event, context):


    #print("-------starting-------")
    #print(event)
    #print("--------ending--------")

    #print("Received event {}".format(event['httpMethod']))

    if event['httpMethod'] == 'POST':
        resp = es_ingest(event)
    else:
        resp = es_search(event)
        
    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    #Add the search results to the response
    response['body'] = resp.text
    #print(resp.text)
    return response

