#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

class Vendor(Resource):
    def get(self):
        vendors = Vendor.query.all()
        response = [vendor.to_dict() for vendor in vendors]
        return response
api.add_resource(Vendor, '/vendors')

class VendorById(Resource):
    def get(self,id):
        vendor = Vendor.query.get(id)
        if vendor is None:
            return {"error": "Vendor not found"}, 404
        return vendor.to_dict()
api.add_resource(VendorById, '/vendors/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
