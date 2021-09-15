import os
from boto3.dynamodb.conditions import Attr
from datamodels.service import get_dynamodb

db = get_dynamodb()
table = db.Table("Interests")


class Interests:
    @staticmethod
    def interest_get(interest):
        print(interest)
        response = table.scan(FilterExpression=Attr("interest").eq(interest))
        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return data
