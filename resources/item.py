from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel 


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="cannot be blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="every item needs a store"
    )
    
    @jwt_required()
    def get(self,name):
        row = ItemModel.getRow(name)
        if row:
            return row.json()
        return {'message': 'Item not found'}, 404
        
    
    @jwt_required()    
    def post(self,name):  
        row = ItemModel.getRow(name)
        ##Check if item exists
        if row:
            return {'message': "Item '{}' already exists".format(name)}, 400
        else:
            data = self.parser.parse_args()
            ##create new item
            item = ItemModel(name, **data)
            try: 
                item.save_to_db()
            except: 
                return {"Server Error": "An error occured inserting '{}'".format(name)}, 500
            return item.json(), 201
        
        
    @jwt_required()    
    def delete(self, name):
        item = ItemModel.getRow(name)
        if item:
            item.delete_from_db()
        return {'message': "item {} Deleted".format(name)}
    
    @jwt_required()    
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.getRow(name)

        try:
            if not item: 
                item = ItemModel(name, **data)
            else: 
                item.price = data['price']
                item.store_id = data['store_id']
            item.save_to_db()
            return item.json(), 200
        except:
            return {"Server Error": "An error occured updating '{}'".format(name)}, 500
        
        
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()] }