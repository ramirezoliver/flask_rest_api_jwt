from flask import jsonify, request
from flask_restful import Resource

from library.app import db
from library.models import Authors
from library.utils.auth_token import token_required


def serialize_author(author: Authors) -> dict:
    author_data = {}
    author_data['name'] = author.name
    author_data['book'] = author.book
    author_data['country'] = author.country
    author_data['booker_prize'] = author.booker_prize
    author_data['id'] = author.id
    return author_data


class CreateAuthor(Resource):
    @token_required
    def post(current_user, self):

        data = request.get_json()

        new_author = Authors(name=data['name'], country=data['country'], book=data['book'], booker_prize=True, user_id=current_user.id)
        db.session.add(new_author)
        db.session.commit()

        return serialize_author(new_author), 201


class GetAuthors(Resource):
    @token_required
    def get(current_user, self):

        authors = Authors.query.filter_by(user_id=current_user.id).all()

        output = []
        for author in authors:
            output.append(serialize_author(author))

        return jsonify({'list_of_authors': output})


class GetAuthor(Resource):
    @token_required
    def get(current_user, self, author_id):

        author = Authors.query.filter_by(id=author_id).first_or_404('Author not found.')

        return serialize_author(author)


class PatchAuthor(Resource):
    @token_required
    def patch(current_user, self, author_id):
        Authors.query.filter_by(id=author_id).first_or_404('Author not found.')

        data = request.get_json()
        schema = set(Authors.__table__.columns.keys())

        if not data or not schema.issuperset(set(data)) or 'id' in data:
            return {'message': 'Forbidden'}, 403

        Authors.query.filter_by(id=author_id).update(data, synchronize_session=False)
        db.session.commit()

        return {'message': 'Update successful'}


class DeleteAuthor(Resource):
    @token_required
    def delete(current_user, self, author_id):
        author = Authors.query.filter_by(id=author_id, user_id=current_user.id).first_or_404('Author not found.')

        db.session.delete(author)
        db.session.commit()

        return {'message': 'Author deleted'}, 202
