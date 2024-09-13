# Import flask's `request` and flask_restx's `Resource` objects.
from flask import request
from flask_restx import Resource

# import other `auth` files
from auth import parsers
from auth import repository
from auth import serializers
from api import api

# define a new namespace called `auth` and set its description.
ns = api.namespace('auth', description='Operations related to authorization')

# create class and end point for user log in
@ns.route('/login')
class Login(Resource):

    # `@api.expect` is used to define the request body that we expect to receive.
    @api.expect(parsers.login_args)
     # `@api.marshal_with` is used to define the response body that we will send back.
    @api.marshal_with(serializers.token)
    def post(self):
        """
        Exchange credentials to access token
        """
        # uses a parser we will define soon called `login_args` to parse the request body and give us the `email` and `password` fields.
        credentials = parsers.login_args.parse_args(request)
        # takes the `email` and `password` field data to `repository`'s login function, which we will define later.
        response = repository.login(
            credentials.get('email'), credentials.get('password'))
        # return a response object which contains the `x-access-token` which is used later to authenticate certain requests
        return {"access_token": response.get("secret")}

# create class and end point for user log out
@ns.route('/logout')
class Logout(Resource):
    # Notice that `@api.doc(security='apiKey')` is used to add a security requirement to this endpoint.
    # This is because we need the `x-access-token` to log out the user.
    @api.doc(security='apiKey')
    def post(self):
        """
        Logout user
        """
        # Logout takes in that `x-access-token` and calls the `logout` function in `repository.py` to log out the user.
        repository.logout(request.headers.get("x-access-token"))
        return {'message': 'Logout successful'}

# create class and end point for user sign up
@ns.route('/signup')
class Signup(Resource):
    @api.expect(parsers.login_args)
    @api.marshal_with(serializers.token)
    def post(self):
        """
        Create user and exchange credentials to access token
        """
        credentials = parsers.login_args.parse_args(request)
        repository.signup(credentials.get('email'),
                          credentials.get('password'))
        response = repository.login(
            credentials.get('email'), credentials.get('password'))
        # return a response object which contains the `x-access-token` which is used later to authenticate certain requests
        return {"access_token": response.get("secret")}

@ns.route('/users')
class Products(Resource):

    @api.doc(security='apiKey')
    def get(self):
        """
        Returns list of users.
        """
        return repository.get_users(request.headers.get("x-access-token"))