from sqlalchemy import func
from .db import db



class CurrencyModel(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    record = db.relationship("RecordModel", uselist=False)
    user = db.relationship("UserModel", uselist=False, back_populates="currency")

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    default_currency_id = db.Column(db.String(128), db.ForeignKey('currency.id'), nullable=True)

    currency = db.relationship('CurrencyModel', back_populates='user')
    record = db.relationship('RecordModel', back_populates='user', lazy="dynamic")

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'default_currency_id': self.default_currency_id}


class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class RecordModel(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.String, primary_key=True)
    cost_amount = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    currency_id = db.Column(db.String, db.ForeignKey('currency.id'), nullable=False)

    user = db.relationship('UserModel', back_populates='record')
    category = db.relationship('CategoryModel', back_populates='record')
    currency = db.relationship("CurrencyModel")

    def to_dict(self):
        return {'id': self.id,
                'cost_amount': self.cost_amount,
                'category_id': self.category_id,
                'user_id': self.user_id,
                'created_at': self.created_at,
                'currency_id': self.currency_id}

