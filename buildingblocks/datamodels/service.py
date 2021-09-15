import boto3
import config


def get_dynamodb():
    return boto3.resource("dynamodb", endpoint_url=config.URL)
