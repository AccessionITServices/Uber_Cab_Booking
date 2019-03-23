import boto3
import requests
def lambda_handler(event, context):
    UBER_ACCESS_TOKEN =' YOUR UBER ACCESS TOKEN'

    s_lat='{}'.format(event["name"])
    dynamodb = boto3.resource('dynamodb')
    table=dynamodb.Table('map')
    response = table.get_item(
    Key={
        '1': '1'
         }
    )
    item = response['Item']
    request_id=item["driver"]
    print(request_id)
    Header ={
      "Authorization": "Bearer %s" % UBER_ACCESS_TOKEN,
      "Content-Type": "application/json"
    }
     
    req=str(request_id)
    url4='https://api.uber.com/v1/requests/%s/map' %\
			(req)
    response4 = requests.get(url4,headers=Header)
    print(response4.status_code)
    if response4 and response4.status_code == 200:
        json_response4 = response4.json()
        print(json_response4)
        link=json_response4["href"]
        print(link)
    return link
