import boto3
import json
import os
from botocore.exceptions import ClientError

SECRET_NAME = os.environ["SECRET_NAME"]
REGION_NAME = os.environ["REGION_NAME"]


def get_secret():
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME,
        endpoint_url='https://secretsmanager.ap-northeast-2.amazonaws.com',
        aws_access_key_id=os.environ['AWS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET']
    )
    secret_value = client.get_secret_value(SecretId=SECRET_NAME)
    secret_value = json.loads(secret_value['SecretString'])
    return secret_value



