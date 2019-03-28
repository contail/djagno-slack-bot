import boto3
import json
import os
from botocore.exceptions import ClientError

REGION_NAME = "ap-northeast-2"


def get_secret():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, 'credentials.json')) as f:
        credentials = json.load(f)
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=REGION_NAME,
            endpoint_url='https://secretsmanager.ap-northeast-2.amazonaws.com',
            aws_access_key_id=credentials['aws_access_key_id'], aws_secret_access_key=credentials['aws_secret_access_key']
        )
        secret_value = client.get_secret_value(SecretId=credentials['SECRET_NAME'])
        secret_value = json.loads(secret_value['SecretString'])
        return secret_value