import os
from datamodels.notesFactory import Notes
from flask import request, json
from flask_restful import Resource
from datamodels.blockFactory import Blocks


# api for getting list of blocks
class ListBlocks(Resource):
    def get(self, dynamodb=None):
        block_list = Blocks.get_blocks()
        return {"status_text": "success", "error_text": {}, "data": block_list}, 200


# api for getting bucket and elements related to each bucket
class ListBuckets(Resource):
    def get(self, dynamodb=None):
        args = request.args
        block_slug = args.get("block_slug")
        user_id = args.get("user_id")
        file_path = os.path.join("static/info.json")
        with open(file_path) as root_file:
            data = json.load(root_file)
        for blocks in data:
            blocks.pop("color")
            blocks.pop("disabled")
            blocks.pop("shortTitle")

        block_data = list(filter(lambda item: item["block_slug"] == block_slug, data))
        is_notes = True
        note_list = []
        if user_id:
            try:
                note_list = Notes.list_notes(user_id)
                note_list.sort(key=lambda item: item["created_date"], reverse=False)
            except:
                is_notes = False
        buckets = block_data[0]["bucket_list"]
        for bucket in buckets:

            bucket["element_list"] = list(
                map(
                    lambda item: {
                        "element_slug": item["element_slug"],
                        "element": item["element"],
                    },
                    bucket["element_list"],
                )
            )
        if is_notes:
            for bucket in block_data[0]["bucket_list"]:
                for elements in range(len(bucket["element_list"])):
                    for notes in range(len(note_list)):
                        if (
                            bucket["element_list"][elements]["element_slug"]
                            == note_list[notes]["element_slug"]
                        ):
                            bucket["element_list"][elements][
                                "lastnote_timestamp"
                            ] = note_list[notes]["created_date"]
        return {"status_text": "success", "error_text": {}, "data": block_data[0]}, 200


# api for getting resources and description related to the element slected
class GetResourceDescription(Resource):
    def get(self, block_slug, bucket_slug, element_slug, dynamodb=None):
        file_path = os.path.join("static/info.json")
        with open(file_path) as root_file:
            data = json.load(root_file)
        for blocks in data:
            blocks.pop("color")
            blocks.pop("disabled")
            blocks.pop("shortTitle")

        block_data = list(filter(lambda item: item["block_slug"] == block_slug, data))

        buckets = block_data[0]["bucket_list"]

        bucket_dictionary = list(
            filter(lambda item: item["bucket_slug"] == bucket_slug, buckets)
        )
        element_list = bucket_dictionary[0]["element_list"]

        selected_element = list(
            filter(lambda item: item["element_slug"] == element_slug, element_list)
        )
        resuorces_description = list(
            map(
                lambda item: {
                    "element": item["element"],
                    "element_slug": item["element_slug"],
                    "resources": item["resources"],
                    "element_description": item["element_description"],
                },
                selected_element,
            )
        )
        element_index = 0
        for indexes in range(len(element_list)):
            if (
                element_list[indexes]["element_slug"]
                == selected_element[0]["element_slug"]
            ):
                element_index += indexes

        resuorces_description.append({"prev_element_slug": ""})
        if element_index != 0:
            resuorces_description[1]["prev_element_slug"] = element_list[
                element_index - 1
            ]["element_slug"]
        resuorces_description.append({"next_element_slug": ""})
        if element_index != (len(element_list) - 1):
            resuorces_description[2]["next_element_slug"] = element_list[
                element_index + 1
            ]["element_slug"]
        resuorces_description.append({"bucket_slug": ""})
        resuorces_description.append({"bucket": ""})
        resuorces_description[3]["bucket_slug"] = bucket_dictionary[0]["bucket_slug"]
        resuorces_description[4]["bucket"] = bucket_dictionary[0]["bucket"]
        return {
            "status_text": "success",
            "error_text": {},
            "data": resuorces_description,
        }, 200


# api for searchng resources with keywords ad filtering it with block_slug and resource_type
class GetResources(Resource):
    def get(self):
        filtersearch_args = request.args
        searched_resource = self.search_resources(filtersearch_args)
        filtered_resource = self.filter_resources(filtersearch_args, searched_resource)
        return {
            "status_text": "success",
            "error_text": {},
            "data": filtered_resource,
        }, 200

    def filter_resources(
        self,
        args,
        searched_resource,
    ):
        filtered_resource = searched_resource
        resource_type = args.get("resource_type")
        block_slug = args.get("block_slug")
        if block_slug:
            filtered_resource = list(
                filter(lambda item: item["block_slug"] == block_slug, filtered_resource)
            )
        if resource_type:
            for blocks in range(len(filtered_resource)):
                block_data = filtered_resource[blocks]
                for elements in range(len(block_data["element_list"])):
                    block_data["element_list"][elements]["resources"] = list(
                        filter(
                            lambda item: resource_type in item["description"],
                            block_data["element_list"][elements]["resources"],
                        )
                    )
            block_data["element_list"] = list(
                filter(lambda item: item["resources"] != [], block_data["element_list"])
            )
        filtered_resource = list(
            filter(lambda item: item["element_list"] != [], filtered_resource)
        )
        return filtered_resource

    def search_resources(self, args):
        search_word = args.get("search_word")
        data = Blocks.get_scan()
        searched_resource = []
        for blocks in range(len(data)):
            block_data = data[blocks]
            element_dic = {}
            element_dic["block_slug"] = block_data["block_slug"]
            element_dic["block"] = block_data["block"]
            element_list = []
            for buckets in block_data["bucket_list"]:
                for elements in buckets["element_list"]:
                    element_list.append(elements)
            element_dic["element_list"] = element_list
            searched_resource.append(element_dic)
        for blocks in range(len(searched_resource)):
            block_data = searched_resource[blocks]
            block_data["element_list"] = list(
                map(
                    lambda item: {
                        "resources": item["resources"],
                        "element_slug": item["element_slug"],
                        "element": item["element"],
                    },
                    block_data["element_list"],
                )
            )
            for elements in range(len(block_data["element_list"])):
                block_data["element_list"][elements]["resources"] = list(
                    filter(
                        lambda item: search_word in item["description"],
                        block_data["element_list"][elements]["resources"],
                    )
                )
            block_data["element_list"] = list(
                filter(lambda item: item["resources"] != [], block_data["element_list"])
            )
        searched_resource = list(
            filter(lambda item: item["element_list"] != [], searched_resource)
        )
        return searched_resource
