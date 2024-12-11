from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config
from api.auth_api import auth_ns
from api.pet_api import pet_ns
from db import Session, create_default_user, revoked_tokens

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

# Define authorizations for Swagger
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* field below: **'Bearer &lt;JWT&gt;'**, where &lt;JWT&gt; is the token"
    }
}

api = Api(app, version='1.0', title='Veterinary API', description='A simple Veterinary API',
          authorizations=authorizations, security='Bearer Auth')

# Call the function to create the default user
create_default_user()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in revoked_tokens

# Register namespaces
api.add_namespace(auth_ns)
api.add_namespace(pet_ns)

if __name__ == '__main__':
    app.run(debug=True) 