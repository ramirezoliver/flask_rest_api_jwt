import datetime
import uuid

import jwt
from flask import current_app as app
from flask import jsonify, make_response, request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from library.app import db
from library.models import Users


class SignUpUser(Resource):
    def post(self):
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'registered successfully'})


class LoginUser(Resource):
    def get(self):

        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = Users.query.filter_by(name=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': str(user.public_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


class GetAllUsers(Resource):
    def post(self):

        users = Users.query.all()

        result = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin

            result.append(user_data)

        return jsonify({'users': result})
