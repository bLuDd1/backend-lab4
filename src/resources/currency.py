import uuid
from flask import jsonify, request, Blueprint
from src import db
from src.models import CurrencyModel
from src.schemas import CurrencySchema
from marshmallow import ValidationError

currency_schema = CurrencySchema()
blueprint_currency = Blueprint('currency', __name__)


@blueprint_currency.post('/currency')
def create_currency():
    currency_data = request.get_json()
    try:
        data = currency_schema.load(currency_data)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    data['id'] = str(uuid.uuid4())
    currency = CurrencyModel(**data)
    try:
        db.session.add(currency)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(currency.to_dict())


@blueprint_currency.get('/currencies')
def get_all_currency():
    currencies = CurrencyModel.query.all()
    return jsonify(currency_schema.dump(currencies, many=True)), 200


@blueprint_currency.delete('/currency/<currency_id>')
def delete_currency(currency_id):
    if not uuid.UUID(currency_id, version=4):
        return jsonify({"error": "Invalid currency_id format"}), 400

    currency = CurrencyModel.query.get(currency_id)
    try:
        db.session.delete(currency)
        db.session.commit()
        return jsonify(currency_schema.dump(currency)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400



