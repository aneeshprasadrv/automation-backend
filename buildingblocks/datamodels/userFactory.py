from datamodels.service import get_dynamodb


db = get_dynamodb()
table = db.Table("User")


class User:
    @staticmethod
    def user_create(userarg):
        response = table.put_item(
            Item={
                "user_id": userarg["user_id"],
                "first_name": userarg["first_name"],
                "last_name": userarg["last_name"],
                "mail_id": userarg["mail_id"],
            },
            ConditionExpression="attribute_not_exists(first_name) AND attribute_not_exists(last_name) AND attribute_not_exists(mail_id)",
        )
        return True

    @staticmethod
    def user_insert(userarg):
        response = table.put_item(
            Item={
                "user_id": userarg["user_id"],
                "first_name": userarg["first_name"],
                "last_name": userarg["last_name"],
                "mail_id": userarg["mail_id"],
                "state_id": userarg["state_id"],
                "district_id": userarg["district_id"],
                "school_id": userarg["school_id"],
                "school_name": userarg["school_name"],
                "job_id": userarg["job_id"],
                "job_role": userarg["job_role"],
                "interest": userarg["interest"],
                "address": userarg["address"],
                "mobile_no": userarg["mobile_no"],
            },
            ConditionExpression="attribute_not_exists(first_name) AND attribute_not_exists(last_name) AND attribute_not_exists(mail_id)",
        )
        return True

    @staticmethod
    def user_update(userarg):
        response = table.update_item(
            Key={
                "user_id": userarg["user_id"],
            },
            UpdateExpression="SET first_name = :first_name, last_name= :last_name, mail_id= :mail_id, state_id= :state_id, district_id= :district_id, school_id= :school_id, school_name= :school_name, job_id= :job_id, job_role= :job_role,interest= :interest,address= :address, mobile_no= :mobile_no",
            ExpressionAttributeValues={
                ":first_name": userarg["first_name"],
                ":last_name": userarg["last_name"],
                ":mail_id": userarg["mail_id"],
                ":state_id": userarg["state_id"],
                ":district_id": userarg["district_id"],
                ":school_id": userarg["school_id"],
                ":school_name": userarg["school_name"],
                ":job_id": userarg["job_id"],
                ":job_role": userarg["job_role"],
                ":interest": userarg["interest"],
                ":address": userarg["address"],
                ":mobile_no": userarg["mobile_no"],
            },
            ReturnValues="UPDATED_NEW",
        )

        return True

    @staticmethod
    def user_get(user_id):
        user = table.get_item(Key={"user_id": user_id})
        return user
