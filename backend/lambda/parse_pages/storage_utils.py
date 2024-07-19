import boto3
from datetime import datetime

def store_unit(unit):
    # First we determine if there is already a unit on the table. 
    current_price = get_current_price(unit)

    # If there is no current price, the unit doesn't exist yet. Let's store it and be done. 
    if current_price is None:
        store_new_unit(unit)
        return 'store_new_unit'
    
    # Has the price changed? Then let's update the data. 
    if current_price != unit['current_price']:
        update_unit_price(unit)
        return 'update_unit_price'
    else:
        return 'no_change'

def update_unit_price(unit):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apartment_listing_data')

    current_date = datetime.today().strftime('%Y-%m-%d')

    response = table.update_item(
        Key={
            'primary_key': unit['primary_key'],
            'secondary_key': unit['secondary_key']
        },
        UpdateExpression='SET price_history = list_append(price_history, :i), current_price = :current_price, last_updated = :last_updated',
        ExpressionAttributeValues={
            ':i': [{ 'price': unit['current_price'], 'date': current_date }],
            ':current_price': unit['current_price'],
            ':last_updated': current_date
        }
    )

def store_new_unit(unit):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apartment_listing_data')

    current_date = datetime.today().strftime('%Y-%m-%d')

    # Add a current price and the day that price was scraped. 
    unit['current_price'] = unit['current_price']
    unit['last_updated'] = current_date

    # Initialize an array for storing the price history. 
    unit['price_history'] = [{ 'price': unit['current_price'], 'date': current_date }]

    # Add the item to dynamoDB. 
    table.put_item(Item=unit)

def get_current_price(unit):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apartment_listing_data')

    response = table.get_item(
        Key={
            'primary_key': unit['primary_key'],
            'secondary_key': unit['secondary_key']
        },
        AttributesToGet=['current_price']
    )

    if 'Item' in response:
        return response['Item']['current_price']
    else:
        return None
    
