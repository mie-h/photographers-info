import json
import ast
from app.db import PHOTOGRAPHERS_INFO_TABLE
from fastapi import HTTPException
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from decimal import Decimal
from app.custom_encoder import CustomEncoder


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response


def get_photographer_dict(photographer):
    photographer_dict = {
        "id": photographer['id'],
        "first_name": photographer['first_name'],
        "last_name": photographer['last_name'],
        "username": photographer['username'],
        "phone_number": photographer['phone_number'],
        "avatar": photographer['avatar'],
        "event_type": photographer['event_type']['type'],
    }
    return photographer_dict


def get_value(value, value_type):
    if value_type == "str":
        return value
    if value_type == "int":
        return int(value)
    if value_type == "list":
        return ast.literal_eval(value)
    if value_type == "float":
        return Decimal(value)


def get_all_photographers():
    data = []
    try:
        response = PHOTOGRAPHERS_INFO_TABLE.scan()
        data = response['Items']
         
        while 'LastEvaluatedKey' in response:
            response = PHOTOGRAPHERS_INFO_TABLE.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error message: {e}")
    body = {
        'data': data
    }
    return build_response(200, body)


def get_photographer_by_id(id):
    try:
        response = PHOTOGRAPHERS_INFO_TABLE.get_item(
            Key={
                'id': id
            }
        )
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error message: {e}")
    
    if 'Item' in response:
        body = {
            'data': response['Item']
        }
        return build_response(200, body)
    else:
        raise HTTPException(status_code=404,
                            detail=f"Photographer with id: {id} was not found")
        

def get_photographers_by_event_type(event_type):
    try:
        data = []
        response = PHOTOGRAPHERS_INFO_TABLE.scan(
            FilterExpression=Attr('event_type.type').contains(event_type)
        )
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = PHOTOGRAPHERS_INFO_TABLE.scan(
                FilterExpression=Attr('event_type.type').contains(event_type),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            data.extend(response['Items'])
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error message: {e}")
    body = {
        'data': data
    }
    return build_response(200, body)


def save_photographer(photographer):
    try:
        photographer = photographer.dict()
        photographer = json.loads(json.dumps(photographer), parse_float=Decimal)
        PHOTOGRAPHERS_INFO_TABLE.put_item(Item=photographer)
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error message: {e}")
    body = {
        'Operation': 'SAVE',
        'Message': 'SUCCESS',
        'Item': photographer
    }
    return build_response(200, body)


def update_photographer(id, key, value, value_type):
    value = get_value(value, value_type)
    if value is None:
        raise HTTPException(status_code=404,
                            detail=f"Error message: value type is invalid")
    keys = key.split(".")
    expression_attribute_names = {}
    for key in keys:
        expression_attribute_names["#" + key] = key
    path = ".".join(expression_attribute_names.keys())
    try:
        response = PHOTOGRAPHERS_INFO_TABLE.update_item(
            Key={
                    'id': id
                },
            UpdateExpression=f'set {path} = :value',
            ExpressionAttributeValues={
                ':value': value
            },
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW")
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")    
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error message: {e}")
    body = {
        'Operation': 'UPDATE',
        'Message': 'SUCCESS',
        'UpdatedAttributes': response
    }
    return build_response(200, body)


def delete_photographer(id):
    try:
        response = PHOTOGRAPHERS_INFO_TABLE.delete_item(
            Key={
                'id': id
            },
            ReturnValues='ALL_OLD'
        )
    except ClientError as e:
        raise HTTPException(status_code=e.response['Error']['Code'],
                            detail=f"Error message: {e}")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error message: {e}")
    body = {
        'Operation': 'DELETE',
        'Message': 'SUCCESS',
        'deletedItem': response
    }
    return build_response(200, body)