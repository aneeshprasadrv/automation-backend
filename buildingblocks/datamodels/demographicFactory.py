from boto3.dynamodb.conditions import Key
from datamodels.service import get_dynamodb


db = get_dynamodb()
school_table = db.Table("Schools")
job_table = db.Table("Jobinterest")


class SchoolData:
    @staticmethod
    def get_states():
        resp = school_table.scan(
            ProjectionExpression="s_id, #s", ExpressionAttributeNames={"#s": "State"}
        )
        data = resp["Items"]
        return data

    @staticmethod
    def get_district(state_id):
        resp = school_table.query(
            IndexName="s_id", KeyConditionExpression=Key("s_id").eq(state_id)
        )
        data = resp["Items"]
        return data

    @staticmethod
    def get_schools(district_id):
        resp = school_table.query(
            IndexName="District_id",
            KeyConditionExpression=Key("District_id").eq(district_id),
        )
        data = resp["Items"]
        return data


class JobData:
    @staticmethod
    def scan_jobroledata():
        response = job_table.scan()
        data = response["Items"]
        return data
