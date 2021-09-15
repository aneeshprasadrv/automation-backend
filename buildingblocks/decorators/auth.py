from functools import wraps
from flask import abort, request
from jose import jwt
import time
from datamodels.userFactory import User


def check_access_token_validity(token):

    claims = jwt.get_unverified_claims(token)
    if time.time() > claims["exp"]:
        print("Token is expired")
        return False

    # check user exists
    try:
        response = User.user_get(claims["sub"])
        return response["Item"]
    except KeyError as e:
        return False


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not "Authorization" in request.headers:
            abort(401)
        user = None
        data = request.headers["Authorization"].encode("ascii", "ignore")
        token = str.replace(str(data, "utf-8"), "Bearer ", "")
        # print(token)
        user = check_access_token_validity(token)
        if user:
            return f(*args, **kws)
        else:
            abort(401)

    return decorated_function
