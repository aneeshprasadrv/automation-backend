from boto3.dynamodb.conditions import Key
from datamodels.service import get_dynamodb


db = get_dynamodb()
blocks = db.Table("Blocks")


class Blocks:
    @staticmethod
    def get_blocks():
        resp = blocks.scan(
            ProjectionExpression="block_slug, #b",
            ExpressionAttributeNames={"#b": "block"},
        )
        data = resp["Items"]
        return data

    @staticmethod
    def get_bucketlist(block_slug):
        response = blocks.query(KeyConditionExpression=Key("block_slug").eq(block_slug))
        data = response["Items"]
        return data

    @staticmethod
    def get_scan():
        resp = blocks.scan()
        data = resp["Items"]
        return data
