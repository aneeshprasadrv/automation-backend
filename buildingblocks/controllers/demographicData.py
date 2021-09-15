from operator import itemgetter
from flask_restful import Resource
from datamodels.service import get_dynamodb
from datamodels.demographicFactory import SchoolData, JobData

db = get_dynamodb()

# api for getting the list of all states
class StateSearch(Resource):
    def get(self, dynamodb=None):
        try:
            data = SchoolData.get_states()
            statelist = [
                dict(tuples) for tuples in {tuple(dic.items()) for dic in data}
            ]
            sorted_statelist = sorted(statelist, key=itemgetter("State"), reverse=False)
            return {
                "status_text": "success",
                "error_text": {},
                "data": sorted_statelist,
            }, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# API for getting districts related to the state selected
class DistrictSearch(Resource):
    def get(self, state_id, dynamodb=None):
        try:
            data = SchoolData.get_district(state_id)
            districts = list(
                map(
                    lambda item: {
                        "district_id": item["District_id"],
                        "district": item["District"],
                    },
                    data,
                )
            )
            district_list = [
                dict(tuples) for tuples in {tuple(dic.items()) for dic in districts}
            ]
            sorted_districtlist = sorted(
                district_list, key=itemgetter("district"), reverse=False
            )
            return {
                "status_text": "success",
                "error_text": {},
                "data": sorted_districtlist,
            }, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for getting list of schools related to "State" and "District" selected
class SchoolSearch(Resource):
    def get(self, district_id, dynamodb=None):
        try:
            data = SchoolData.get_schools(district_id)
            schools = list(
                map(
                    lambda item: {
                        "school_id": item["School_id"],
                        "school_name": item["Schools"],
                        "school_phone": item["School_phn"],
                        "school_website": item["School_website"],
                        "zip_code": item["mzip"],
                    },
                    data,
                )
            )
            school_list = sorted(schools, key=itemgetter("school_name"), reverse=False)
            return {
                "status_text": "success",
                "error_text": {},
                "data": school_list,
            }, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for getting list of job_levels
class JobLevellist(Resource):
    def get(self, dynamodb=None):
        try:
            data = JobData.scan_jobroledata()
            jobs = data[0]["job_level"]
            job_levellist = list(
                map(
                    lambda item: {
                        "job_id": item["job_id"],
                        "job_name": item["job_name"],
                    },
                    jobs,
                )
            )
            return {
                "status_text": "success",
                "error_text": {},
                "data": job_levellist,
            }, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for getting job_roles related to job_level selected
class JobRolelist(Resource):
    def get(self, job_id, dynamodb=None):
        try:
            data = JobData.scan_jobroledata()
            jobs = data[0]["job_level"]
            job_roles = list(filter(lambda item: item["job_id"] == job_id, jobs))
            job_rolelist = list(map(lambda item: item["job_role"], job_roles))
            return {
                "status_text": "success",
                "error_text": {},
                "data": job_rolelist[0],
            }, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500
