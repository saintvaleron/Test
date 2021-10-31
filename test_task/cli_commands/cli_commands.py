from flask import Blueprint
import pandas as pd

from config import Config
from test_task.models import db, Products, Reviews

cli_commands = Blueprint('cli_commands', __name__, cli_group=None)


@cli_commands.cli.command('transfer_from_csv_to_db')
def transfer_from_csv_to_db():
    df_products = pd.read_csv(f'{Config.STATIC_FOLDER}/csv_files/Products.csv', delimiter=',')
    df_reviews = pd.read_csv(f'{Config.STATIC_FOLDER}/csv_files/Reviews.csv', delimiter=',')
    buffer = []

    for index, row in df_products.iterrows():
        buffer.append({'asin': row['Asin'], 'title': row['Title']})

        if len(buffer) >= 10000:
            db.session.bulk_insert_mappings(Products, buffer)
            buffer = []

    db.session.bulk_insert_mappings(Products, buffer)
    db.session.commit()

    products = Products.query.all()

    buffer = []
    products2ids = {}

    for product in products:
        products2ids[product.asin] = product.id

    for index, row in df_reviews.iterrows():

        if products2ids.get(row['Asin']) is None:
            continue

        buffer.append({'product_id': products2ids.get(row['Asin']), 'review': row['Review'], 'title': row['Title']})

        if len(buffer) >= 10000:
            db.session.bulk_insert_mappings(Reviews, buffer)
            buffer = []

    db.session.bulk_insert_mappings(Reviews, buffer)
    db.session.commit()
