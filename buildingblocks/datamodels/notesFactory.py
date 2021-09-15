from datetime import datetime
import uuid
from boto3.dynamodb.conditions import Attr, Key
from datamodels.service import get_dynamodb
import datetime
import dateutil.tz

eastern = dateutil.tz.gettz('US/Eastern')


db = get_dynamodb()
table = db.Table("Notes")


class Notes:
    @staticmethod
    def add_note(note_args):
        note = table.put_item(
            Item={
                "note_id": str(uuid.uuid4()),
                "user_id": note_args["user_id"],
                "block_slug": note_args["block_slug"],
                "bucket_slug": note_args["bucket_slug"],
                "element_slug": note_args["element_slug"],
                "note_type": note_args["note_type"],
                "note": note_args["note"],
                "created_date": str(datetime.datetime.now(tz=eastern).strftime("%d %B %Y  %I:%M %P")),
            },       
        )
        return {"success": True}

    @staticmethod
    def edit_note(note_args):
        updated_note = table.put_item(
            Item={
                "note_id": note_args["note_id"],
                "user_id": note_args["user_id"],
                "block_slug": note_args["block_slug"],
                "bucket_slug": note_args["bucket_slug"],
                "element_slug": note_args["element_slug"],
                "note_type": note_args["note_type"],
                "note": note_args["note"],
                "created_date": str(datetime.datetime.now(tz=eastern).strftime("%d %B %Y  %I:%M %P")),
            },
        )
        return {"success": True}

    @staticmethod
    def del_note(note_id):
        note = table.delete_item(
            Key={"note_id": note_id}, ConditionExpression="attribute_exists(note_id)"
        )
        return True

    @staticmethod
    def list_notes(user_id):
        pagination_key = None
        query_params = {
            "IndexName": "user_id",
            "KeyConditionExpression": Key("user_id").eq(user_id),
        }
        if pagination_key:
            query_params["ExclusiveStartKey"] = pagination_key
        query_response = table.query(**query_params)
        data = query_response["Items"]
        return data

    @staticmethod
    def saved_notes(user_id, bucket_slug, element_slug):
        pagination_key = None
        query_params = {
            "IndexName": "user_id",
            "KeyConditionExpression": Key("user_id").eq(user_id),
            "FilterExpression": Attr("bucket_slug").eq(bucket_slug)
            and Attr("element_slug").eq(element_slug),
        }
        if pagination_key:
            query_params["ExclusiveStartKey"] = pagination_key
        query_response = table.query(**query_params)
        data = query_response["Items"]
        return data
