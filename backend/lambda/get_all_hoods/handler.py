import boto3
import json
import zlib

# Eventually moving this to a layer!
def get_listing_data():
    client = boto3.client('s3')
    
    response = client.get_object(
        Bucket='chicago-apartment-data',
        Key='listing-data'
    )

    return json.loads(zlib.decompress(response['Body'].read()))

"""
this lambda gives back an array of all of the hoods!
"""
def handler(event, context):
    units = get_listing_data()

    neighborhoods = set()
    for unit in units:
        neighborhoods |= set(unit['neighborhoods'])
    
    return list(neighborhoods)
    

    

