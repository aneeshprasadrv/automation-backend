from flask import Flask, request, jsonify


class ValidationError(Exception):
    def __init__(self, error=None, message='Invalid input'):
        self.error = error
        self.message = message

def API_SUCCESS(msg="Success", payload=None):
    response = {
        'status': 'Success',
        'message': msg
    }
    if payload is not None:
        response['payload'] = payload
    return jsonify(response)

def API_ERROR(msg, error=None):
    response = {
        'statusCode': 500,
        'status_text': 'Error',
        'data': msg,
    }
    if error is not None:
        response['data'] = msg,error
    return jsonify(response)

def ValidateRequest(schema):
    def decorator(func):
        def decorated_function(*args, **kwargs):
            validation_result = schema.validate(request.json)
            if validation_result.get('success', False) is False:
                raise ValidationError(
                  validation_result.get('error'))
            request.validated_json = validation_result.get('data')
            return func(*args, **kwargs)
        return decorated_function
    return decorator