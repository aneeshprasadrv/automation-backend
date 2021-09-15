from operator import itemgetter
from kanpai import Kanpai
from flask_restful import Resource
from flask import request
from datamodels.userFactory import User
from datamodels.interestsFactory import Interests
from decorators.validation import ValidateRequest


# creating user profile
class UserCreate(Resource):

    REQUEST_SCHEMA = Kanpai.Object(
        {
            "user_id": Kanpai.String().trim().required("User Id is required"),
            "mail_id": Kanpai.Email().required().required("Mail Id is required"),
            "first_name": Kanpai.String().required("First Name is required"),
            "last_name": Kanpai.String(),
        }
    )

    @ValidateRequest(schema=REQUEST_SCHEMA)
    def post(self, dynamodb=None):
        args = request.validated_json
        try:
            response = User.user_get(args["user_id"])
            return {"status_text": "success", "data": response["Item"]}, 200
        except KeyError as e:
            try:
                response = User.user_create(args)
                return {
                    "status_text": "success",
                    "data": "User has been created successfully",
                }, 201
            except Exception as err:
                return {
                    "status_text": "error",
                    "data": "HTTPStatusCode:{}, {}".format(
                        err.response["ResponseMetadata"]["HTTPStatusCode"], err
                    ),
                }, 500
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# for updating user profile
class UserUpdate(Resource):

    REQUEST_SCHEMA = Kanpai.Object(
        {
            "user_id": Kanpai.String().trim().required("User Id is required"),
            "mail_id": Kanpai.Email().required(),
            "first_name": Kanpai.String().required("First Name is required"),
            "last_name": Kanpai.String(),
            "state_id": Kanpai.String().required("State ID is required"),
            "district_id": Kanpai.String(),
            "school_id": Kanpai.String(),
            "school_name": Kanpai.String(),
            "job_id": Kanpai.String().required("Job Id is required"),
            "job_role": Kanpai.String().required("Job role is required"),
            "interest": Kanpai.String().required("Interest is required"),
            "address": Kanpai.String(),
            "mobile_no": Kanpai.String(),
        }
    )

    # for updating the user details
    @ValidateRequest(schema=REQUEST_SCHEMA)
    def put(self, dynamodb=None):
        try:
            response = User.user_update(request.validated_json)
            return {
                "status_text": "success",
                "data": "User details has been updated successfully",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for listing the users
class GetUser(Resource):
    def get(self, user_id, dynamodb=None):
        try:
            response = User.user_get(user_id)
            return {"status_text": "success", "data": response["Item"]}, 200
        except KeyError as e:
            return {
                "status_text": "error",
                "data": "There is no user created in this ID",
            }, 500
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api to get user recommendations
class GetUserInterests(Resource):
    def get(self, user_id, dynamodb=None):
        try:
            response = User.user_get(user_id)
            interest_list = response["Item"]["interest"].split(",")
            sorted_interestlist = []
            for interest in interest_list:
                interest_data = Interests.interest_get(interest.strip())
                interestlist = [
                    dict(tuples)
                    for tuples in {tuple(dic.items()) for dic in interest_data}
                ]
                sorted_interestlist.append(
                    sorted(interestlist, key=itemgetter("interest"), reverse=False)
                )
            return {"status_text": "success", "data": sorted_interestlist}, 200
        except KeyError as e:
            print(e)
            return {
                "status_text": "error",
                "data": "No interest recommendation found for the user",
            }, 500

        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500
