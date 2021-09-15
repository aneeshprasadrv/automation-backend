from slugify import slugify
import os
from flask import json


file_path = os.path.join("info.json")
with open(file_path) as root_file:
    data = json.load(root_file)
for dic in data:
    dic["bucket_list"]= dic.pop("categories")
    dic["block_slug"]=dic.pop("slug")
    dic["block"]=dic.pop("title")
    dic["prev_blockslug"]=dic.pop("prev")
    dic["next_blockslug"]=dic.pop("next")  
    for i in dic["bucket_list"]:
        i["bucket_slug"]=i.pop("slug")
        i["bucket"]=i.pop("title")
        i["prev_bucketslug"]=i.pop("prev")
        i["next_bucketslug"]=i.pop("next")        
        i["element_list"]=i.pop("bullets")
        for b in i["element_list"]:
            b["element_description"]=b.pop("considerations")
            b["element"]=b.pop("description")
            b["element_slug"]= slugify(b["element"][4:], to_lower=True, max_length=100)
                    
file_path = os.path.join("buildingblocks.json")
with open(file_path, "w") as outfile:
    json.dump(data, outfile)
    print("success")