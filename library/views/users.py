from flask_restful import Resource
from library.app import db
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from library.models import Users
from library.app import db
from flask import current_app as app

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
            token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token}) 

        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


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