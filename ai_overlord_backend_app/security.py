import logging
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


auth = HTTPBasicAuth()
token_expire = 50000 #


secret_key = "this needs to change and not be in the code like this"  # todo: must be dependant of some outside conf.


def generate_auth_token(id, expiration=50000):
    s = Serializer(secret_key, expires_in=expiration)
    token = s.dumps({'id': id})
    logging.debug("token created: " + str(token) + "id: " + id)
    return token


def verify_auth_token(token):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data['id']
