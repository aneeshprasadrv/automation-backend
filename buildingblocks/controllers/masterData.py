import os
from decimal import Decimal
from flask import json, request
from flask_restful import Resource
from datamodels.service import get_dynamodb

db = get_dynamodb()


class HealthCheck(Resource):
    def get(self):
        return {"Health": "Good"}


# api for getting mainblock details as response
class MainInfo(Resource):
    def get(self):
        try:
            file_path = os.path.join("static/info.json")
            with open(file_path) as root_file:
                data = json.load(root_file)

            return data, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# API for appending job roles and interests
class InsertJobinterest(Resource):
    def get(self, dynamodb=None):
        try:
            file_path = os.path.join("static/role.json")
            with open(file_path) as json_file:
                demo_list = json.load(json_file, parse_float=Decimal)
            jobtable = db.Table("Jobinterest")
            for demos in demo_list:
                jobtable.put_item(Item=demos)
                return {
                    "status_text": "success",
                    "data": "Jobinterest table has been updated",
                }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# API for updating the school data
class InsertSchooldata(Resource):
    def get(self, dynamodb=None):
        try:
            request_args = request.args
            file_count = request_args.get("file_count")
            if file_count:
                file_path = "static/schooldata_" + str(file_count) + ".json"
            else:
                file_path = "static/schooldata.json"
            with open(file_path) as json_file:
                school_list = json.load(json_file, parse_float=Decimal)
            schooldata = db.Table("Schools")
            with schooldata.batch_writer() as batch:
                for demos in school_list:
                    batch.put_item(Item=demos)
            return {"status_text": "success", "data": "updated table"}, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500



# api for appending blocks table
class InsertBlocks(Resource):
    def get(self, dynamodb=None):
        try:
            Blocks = db.Table("Blocks")
            file_path = os.path.join("static/buildingblocks.json")
            with open(file_path) as json_file:
                block_list = json.load(json_file, parse_float=Decimal)
            for demos in block_list:
                Blocks.put_item(Item=demos)
            return {
                "status_text": "success",
                "data": "Blocks table has been updated",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for appending interests table
class InsertInterests(Resource):
    def get(self, dynamodb=None):
        try:
            Interests = db.Table("Interests")
            file_path = os.path.join("static/interest.json")
            with open(file_path) as json_file:
                interest_list = json.load(json_file, parse_float=Decimal)
            for demos in interest_list:
                Interests.put_item(Item=demos)
            return {
                "status_text": "success",
                "data": "Interests table has been updated",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500
