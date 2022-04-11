from functools import wraps

import jwt
from flask import current_app as app
from flask import jsonify, request
from flask_restful import Resource

from library.app import db
from library.models import Authors, Users


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


class CreateAuthor(Resource):
    @token_required
    def post(current_user, self):

        data = request.get_json()

        new_authors = Authors(name=data['name'], country=data['country'], book=data['book'], booker_prize=True, user_id=current_user.id)
        db.session.add(new_authors)
        db.session.commit()

        return jsonify({'message': 'new author created'})


class GetAuthors(Resource):
    @token_required
    def get(current_user, self):

        authors = Authors.query.filter_by(user_id=current_user.id).all()

        output = []
        for author in authors:

            author_data = {}
            author_data['name'] = author.name
            author_data['book'] = author.book
            author_data['country'] = author.country
            author_data['booker_prize'] = author.booker_prize
            output.append(author_data)

        return jsonify({'list_of_authors': output})


class DeleteAuthor(Resource):
    @token_required
    def delete(current_user, self, author_id):
        author = Authors.query.filter_by(id=author_id, user_id=current_user.id).first()
        if not author:
            return jsonify({'message': 'author does not exist'})

        db.session.delete(author)
        db.session.commit()

        return jsonify({'message': 'Author deleted'})
