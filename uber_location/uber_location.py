import json
import boto3
from boto3.dynamodb.conditions import Key,Attr

def sow(event, context):
    s_lat='{}'.format(event["name"])
    s_lng='{}'.format(event["email"])
   
    print(s_lat+"  "+s_lng)
    dynamodb = boto3.resource('dynamodb')
    table=dynamodb.Table('location')
    response=table.put_item(
    Item={
        "id":'1',
        "lattitude":s_lat,
        "longitude":s_lng
    }
)