from flask import request
from flask_restful import Resource


class AuthenticatedResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        headers = request.headers
        if 'Authorization' in headers:
            auth_header = headers['Authorization']
            jwt_token = auth_header.split("Bearer ")[1]
            # Confirm token is actually linked to active token on server side
            # some sort of cache to save tokens?  Maybe DB, easiest to use cache
            super(AuthenticatedResource, self).dispatch_request(*args, **kwargs)
        else:
            return {'message': 'Unauthorized'}, 401

