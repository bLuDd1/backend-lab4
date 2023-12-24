import uuid
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from passlib.hash import pbkdf2_sha256
from src import db
from src.models import UserModel, CurrencyModel
from src.schemas import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()
blueprint_user = Blueprint('users', __name__)


@blueprint_user.get('/user/<user_id>')
@jwt_required()
def get_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        return jsonify(user_schema.dump(user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@blueprint_user.delete('/user/<user_id>')
@jwt_required()
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@blueprint_user.post('/register')
def register_user():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    data['id'] = uuid.uuid4().hex
    data['password'] = pbkdf2_sha256.hash(data['password'])
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify(error=str(e)), 401
    return jsonify(user.to_dict())


@blueprint_user.post('/login')
def login_user():
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = UserModel.query.filter_by(name=data['name']).first()

    if user and pbkdf2_sha256.verify(data['password'], user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(error='Invalid username or password'), 400


@blueprint_user.get('/users')
@jwt_required()
def get_users():
    users = UserModel.query.all()
    return jsonify(user_schema.dump(users, many=True))
