import boto3

DYNAMODB_TABLE_NAME = 'photographers-info'
DYNAMODB = boto3.resource('dynamodb', 
                          region_name='us-west-1')
PHOTOGRAPHERS_INFO_TABLE = DYNAMODB.Table(DYNAMODB_TABLE_NAME)