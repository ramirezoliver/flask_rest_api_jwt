from flask import Blueprint
from flask_restful import Api

from library.views.authors import (CreateAuthor, DeleteAuthor, GetAuthor,
                                   GetAuthors, PatchAuthor)
from library.views.users import GetAllUsers, LoginUser, SignUpUser

authors_bp = Blueprint('authors_bp', __name__)
users_bp = Blueprint('users_bp', __name__)

authors_api = Api(authors_bp)
users_api = Api(users_bp)

users_api.add_resource(SignUpUser, '/register')
users_api.add_resource(LoginUser, '/login')
users_api.add_resource(GetAllUsers, '/users')

authors_api.add_resource(CreateAuthor, '/author')
authors_api.add_resource(GetAuthors, '/authors')
authors_api.add_resource(GetAuthor, '/author/<author_id>')
authors_api.add_resource(PatchAuthor, '/author/<author_id>')
authors_api.add_resource(DeleteAuthor, '/author/<author_id>')
