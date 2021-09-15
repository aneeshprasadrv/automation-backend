from copy import Error
from botocore.exceptions import ClientError
from flask_restful import Resource
from datamodels.service import get_dynamodb


db = get_dynamodb()


class CreateTables(Resource):
    def get(self):
        table_val = self.create_demotable()
        table_val = self.create_schtable()
        table_val = self.create_usertable()
        table_val = self.create_notes()
        table_val = self.create_blocks()
        table_val = self.create_interests()

        if table_val == None:
            return {"message": "All tables have been created already"}
        else:
            return table_val.table_status, 200

    # table for saving job roles and interests
    def create_demotable(dynamodb=None):
        try:
            table = db.create_table(
                TableName="Jobinterest",
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table

    # table for saving school data
    def create_schtable(dynamodb=None):
        try:
            table = db.create_table(
                TableName="Schools",
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                    {
                        "AttributeName": "s_id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                    {
                        "AttributeName": "District_id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "s_id",
                        "KeySchema": [
                            {"AttributeName": "s_id", "KeyType": "HASH"},
                        ],
                        "Projection": {
                            "ProjectionType": "INCLUDE",
                            "NonKeyAttributes": ["State", "District_id", "District"],
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 10,
                            "WriteCapacityUnits": 10,
                        },
                    },
                    {
                        "IndexName": "District_id",
                        "KeySchema": [
                            {"AttributeName": "District_id", "KeyType": "HASH"},
                        ],
                        "Projection": {
                            "ProjectionType": "INCLUDE",
                            "NonKeyAttributes": [
                                "District",
                                "School_id",
                                "Schools",
                                "School_phn",
                                "School_website",
                                "mzip",
                            ],
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 10,
                            "WriteCapacityUnits": 10,
                        },
                    },
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table

    # table for saving user details
    def create_usertable(dynamodb=None):
        try:
            table = db.create_table(
                TableName="User",
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "user_id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table

    # table for saving created notes by user
    def create_notes(dynamodb=None):
        try:
            table = db.create_table(
                TableName="Notes",
                KeySchema=[
                    {"AttributeName": "note_id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "note_id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                    {
                        "AttributeName": "user_id",
                        # AttributeType defines the data type.
                        "AttributeType": "S",
                    },
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "user_id",
                        "KeySchema": [
                            {"AttributeName": "user_id", "KeyType": "HASH"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 10,
                            "WriteCapacityUnits": 10,
                        },
                    }
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table

    def create_blocks(dynamodb=None):
        try:
            table = db.create_table(
                TableName="Blocks",
                KeySchema=[
                    {"AttributeName": "block_slug", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "block_slug",
                        "AttributeType": "S",
                    },
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table

    def create_interests(dynamodb=None):
        try:
            table = db.create_table(
                TableName="Interests",
                KeySchema=[
                    {"AttributeName": "interest_slug", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "interest_slug",
                        "AttributeType": "S",
                    },
                ],
                ProvisionedThroughput={
                    # ReadCapacityUnits set to 10 strongly consistent reads per second
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,  # WriteCapacityUnits set to 10 writes per second
                },
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return table
