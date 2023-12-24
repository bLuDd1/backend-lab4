from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    default_currency_id = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    category_id = fields.UUID(required=True)
    created_at = fields.DateTime(dump_only=True)
    cost_amount = fields.Integer(required=True)
    currency_id = fields.UUID(required=True)


class CurrencySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)

