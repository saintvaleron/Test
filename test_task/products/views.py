import json

from flask import Blueprint, request
from psycopg2 import DatabaseError, DataError

from config import Config
from test_task.models import Products, Reviews, db

products = Blueprint('products', __name__, template_folder='templates', static_folder='static', url_prefix='/')


@products.route('products/get/<int:prod_id>/<int:page>', methods=['GET'])
def get_product(prod_id, page):
    product = Products.query.filter(Products.id == prod_id).first()
    reviews = [row.to_dict() for row in product.product_review]
    offset = (page - 1) * Config.PRODUCT_PER_PAGE
    limit = offset + Config.PRODUCT_PER_PAGE

    if product is not None:
        return json.dumps({
            'asin': product.asin,
            'title': product.title,
            'reviews': reviews[offset:limit]
        }), 200

    return json.dumps({
        'status': 'error',
        'message': 'Product does not exist'
    }), 404


@products.route('review/add', methods=['PUT'])
def add_review():
    data = request.json
    product = Products.query.filter(Products.id == int(data['id'])).first()

    if product is not None:
        try:
            new_review = Reviews(
                review=data['review'],
                product_id=product.id
            )

            db.session.add(new_review)
            db.session.commit()

        except (DatabaseError, DataError) as error:
            return json.dumps({'status': 'error', 'message': error}), 500
    else:
        return json.dumps({'status': 'error', 'message': 'Product does not exist'}), 404

    return json.dumps({'status': 'ok'}), 200
