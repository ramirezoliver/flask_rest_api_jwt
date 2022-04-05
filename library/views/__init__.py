from flask import Blueprint
from flask_restful import Api

from library.views.users import SignUpUser, LoginUser, GetAllUsers

users_bp = Blueprint('users_bp', __name__)

users_api = Api(users_bp)

users_api.add_resource(SignUpUser, '/register')
users_api.add_resource(LoginUser, '/login')
users_api.add_resource(GetAllUsers, '/users')