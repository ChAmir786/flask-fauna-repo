from flask import Flask, Blueprint
from api import api
# Import the namespace we just created
from auth.controller import ns as auth_namespace
from faunadb import errors as faunaErrors

@api.errorhandler(faunaErrors.BadRequest)
def fauna_error_handler(e):
    return {'message': e.errors[0].description}, 400


@api.errorhandler(faunaErrors.Unauthorized)
@api.errorhandler(faunaErrors.PermissionDenied)
def fauna_error_handler(e):
    return {'message': "Access forbidden"}, 403
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)

# Add the auth namespace to the API
api.add_namespace(auth_namespace)
# flask_app.register_blueprint(blueprint)


app.register_blueprint(blueprint)

def main():
    app.run(debug=False)


if __name__ == "__main__":
    main()