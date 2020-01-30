from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json, 200

        return {'message': 'no item found with that name'}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except RuntimeError:
            return {"message": "An error occurred inserting the item."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
