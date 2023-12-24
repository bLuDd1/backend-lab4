import uuid
from flask import jsonify, request, Blueprint
from src import db
from src.models import UserModel
from src.schemas import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()
blueprint_user = Blueprint('users', __name__)


@blueprint_user.get('/user/<user_id>')
def get_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        return jsonify(user_schema.dump(user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@blueprint_user.delete('/user/<user_id>')
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@blueprint_user.post('/user')
def create_user():
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data['id'] = uuid.uuid4().hex
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify(error=str(e)), 400
    return jsonify(user.to_dict())


@blueprint_user.get('/users')
def get_users():
    users = UserModel.query.all()
    return jsonify(user_schema.dump(users, many=True))
