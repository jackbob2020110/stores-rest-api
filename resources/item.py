from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
    )
    
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id."
    )

    @jwt_required()
    # GET
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404
    
    # Create
    def post(self,name):
        # 判断是否已经存在
        if ItemModel.find_by_name(name):  #next(filter(lambda x: x['name'] == name,items), None) is not None:
            return {'message': "An item with name'{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
      
        # 获取POST的BODY数据
        #data = request.get_json()
        item = ItemModel(name,**data)
        
        try:
            #ItemModel.insert(item)
            item.save_to_db()
        except:
            return {'message':'An error occurred inserting the item.'}, 500 # Internal Server Error

        return item.json(), 201
  
        
    #HTTP DELETE
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'item was deleted'}


    #HTTP PUT
    def put(self,name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            data = ItemModel(name, **data)
        else:
             item.price = data['price']
        
        item.save_to_db()

        return item.json()

   

class ItemList(Resource):
    def get(self):
        
        # Method 1:
        return {'items': [x.json() for x in ItemModel.query.all()]}
        
        # Method 2:
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}