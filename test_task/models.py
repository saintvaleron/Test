from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT
from sqlalchemy import Index

db = SQLAlchemy()


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(VARCHAR(2048))
    asin = db.Column(VARCHAR(128))
    product_review = db.relationship('Reviews', backref='products', lazy=True)


Index('iproductasin', Products.asin)


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer(), primary_key=True)
    review = db.Column(TEXT)
    title = db.Column(VARCHAR(2048))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'review': self.review
        }
