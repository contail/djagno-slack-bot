import boto3
import json
import os
from botocore.exceptions import ClientError

def get_secret():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, 'keys.json')) as f:
        credentials = json.load(f)
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=os.environ['REGION_NAME'],
            endpoint_url='https://secretsmanager.ap-northeast-2.amazonaws.com',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
        secret_value = client.get_secret_value(SecretId=os.environ['SECRET_NAME'])
        secret_value = json.loads(secret_value['SecretString'])
        return secret_value