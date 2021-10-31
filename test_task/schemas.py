from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from test_task.models import Products, Reviews


class ProductsSchema(SQLAlchemySchema):
    class Meta:
        model = Products
        load_instance = True
        include_relationships = True

    id = auto_field()
    title = auto_field()
    asin = auto_field()


class ReviewsSchema(SQLAlchemySchema):
    class Meta:
        model = Reviews
        load_instance = True
        include_relationships = True

    id = auto_field()
    review = auto_field()
    product_id = auto_field()
