import boto3
import logging
import os
import time
import requests
import urllib
from boto3.dynamodb.conditions import Key,Attr

logger=logging.getLogger()
logger.setLevel(logging.DEBUG)


"""---Main handler---"""
UBER_SERVER_TOKEN ='UBER SERVER TOKEN'
UBER_ACCESS_TOKEN ='UBER ACCESS TOKEN'

Header ={
      "Authorization": "Bearer %s" % UBER_ACCESS_TOKEN,
      "Content-Type": "application/json"
    }
     

def lambda_handler(event,context):
    os.environ['TZ']='Asia/Kolkata'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    print(event)
    
    return dispatch(event)
    
def dispatch(intent_request):
    #print(intent_request)
    intent_name=intent_request['currentIntent']['name']
    #print (intent_name)
    if intent_name =="BookCar":
        return ubercab(intent_request)
    elif intent_name =="conform_book":
        return confirm(intent_request)
    elif intent_name == "cancel":
        return cancel(intent_request)

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def ubercab(intent_request):
    global request_id,s_lat,s_lng,e_lat,e_lng,pool_product_id
    session_attributes={}
    destination = intent_request['currentIntent']['slots']['PickUpCity']
    num= intent_request['currentIntent']['slots']['cartypes']
    number=int(num)
    print(number)
    dynamodb = boto3.resource('dynamodb')
    table=dynamodb.Table('location')
    response = table.get_item(
    Key={
        'id': '1'
         }
    )
    item = response['Item']
    print(item)
    s_lat=item["lattitude"]
    s_lng=item["longitude"]
    
   
    print(s_lat+"   "+ s_lng)
    
    api_key = None
    
    GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
    if api_key is not None:
      geocode_url=geocode_url+"&key={GOOGLE API KEY ID}".format(api_key)
    parameters1 = {
        'address':destination
    }
    req = requests.get(GOOGLE_MAPS_API_URL, params=parameters1)
    res = req.json()
    
    result = res['results'][0]
    
    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']
    
    e_lat='{lat}'.format(**geodata)
    print(e_lat)
    e_lng='{lng}'.format(**geodata)
    print(e_lng)
    
   
    if number==1:
        name="UberAuto"
    elif number==2:
        name="UberGo"
    elif number==3:
        name="Premier"
    elif number==4:
        name="UberXL"
    elif number==5:
        name="Hire Go"
    elif number==6:
        name="Hire Premier"
    elif number==7:
        name="Hire XL"
    
    #print(name)
    
    url1 = "https://api.uber.com/v1/products?latitude=%s&longitude=%s&server_token=%s" %\
          (s_lat,s_lng, UBER_SERVER_TOKEN)
    response1 = requests.get(url1)
    if response1 and response1.status_code == 200:
            json_response1 = response1.json()
            print(json_response1)
            for product in json_response1["products"]:
              if product['display_name']==name:
                  pool_product_id = product["product_id"]
            print('product id is:'+pool_product_id)
    
    
    url2 = "https://api.uber.com/v1/requests/estimate"
    parameters2 = {
                "start_latitude":s_lat,
                "start_longitude":s_lng,
                "end_latitude":e_lat,
                "end_longitude":e_lng,
                "product_id":pool_product_id 
                }
    response2 = requests.post(url2, json=parameters2, headers=Header)
    
    if response2 and response2.status_code == 200:
        json_response2 = response2.json()
        #print(json_response2)
        cost=json_response2["price"]["display"]
        print('estimated price:'+cost)
        time=json_response2["trip"]['duration_estimate']
        print('travel time:')
        print(time)
        pickup=str(json_response2['pickup_estimate'])
        print("estimated pickup:")
        print(pickup)
        
    if response2.status_code == 200:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "do you really want to book a cab from"+destination+"with car type"+name+"estimated price:"+cost+"estimated pickup is:"+pickup
            }
        )
    elif  response2.status_code == 404:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "An invalid product ID was requested. Could not find a default product."
            }
        )
    elif  response2.status_code == 422:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "Distance between start and end location exceeds 100 miles or Pickup and Dropoff can’t be the same or The destination is not supported ."
            }
        )
    elif response2.status_code == 403:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "Trip estimates not allowed while the user is currently on a trip."
            }
        )
    else:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "problem in processing your requests"
            }
        )
def confirm(intent_request):
    global request_id
    
    session_attributes={}
    url3="https://api.uber.com/v1/requests"
    parameters3 = {
              #"fare_id": idd,
              "product_id": pool_product_id, 
              "start_latitude":s_lat,
              "start_longitude":s_lng,
              "end_latitude":e_lat,
              "end_longitude":e_lng
                
              }
    response3 = requests.post(url3, json=parameters3, headers=Header)
   
    
    if response3 and response3.status_code == 202:
        json_response3 = response3.json()
        request_id = json_response3['request_id']
        print("request_id:"+request_id)
        dynamodb = boto3.resource('dynamodb')
        table=dynamodb.Table('map')
        response=table.put_item(
        Item={
            "1":'1',
            "driver":request_id
             }
        )
    
    if response3.status_code == 202:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "congratulations,your cab have been booked successfullyy."
            }
        )
    elif  response3.status_code == 404:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "An invalid product ID was requested. Retry the API call with a valid product ID."
            }
        )
    elif  response3.status_code == 422:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "Distance between start and end location exceeds 100 miles or Pickup and Dropoff can’t be the same or The destination is not supported."
            }
        )
    elif response3.status_code == 403:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "user_not_allowed or too_many_cancellations"
            }
        )
    elif response3.status_code == 409:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "The rider must have at least one payment method or The user is currently on a trip"
            }
        )
    
    elif  response3.status_code == 400:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "you have some payment issues please visit uber help"
            }
        )
    elif  response3.status_code == 500:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "An unknown error has occurred"
            }
        )
    else:
        return close(
            session_attributes,
            'Fulfilled', 
            {
                'contentType': 'PlainText',
                'content': "sorry,there is problem in processing your request.please try after some time"
            }
        )
   
def cancel(intent_request):
    session_attributes={}
    req=str(request_id)
    print(req)
    url='https://api.uber.com/v1/requests/%s' %\
            (req)
    response = requests.delete(url,headers=Header)
    print(response.status_code)
      
    if response.status_code == 204:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "OK,your ride has been cancelled."
            }
        )
    elif response.status_code == 404:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "User is not currently on a trip."
            }
        )
    elif response.status_code == 403:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "Forbidden or Trips using the cash payment method must be canceled by the driver."
            }
        )
    else:
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': "There is a problem in processing your request"
            }
        )


    
