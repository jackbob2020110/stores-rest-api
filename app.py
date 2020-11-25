from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# 导入资源模块
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False

app.secret_key = 'mydemo'
api = Api(app)





jwt = JWT(app, authenticate, identity) # /auth

       
# 第一个参数是添加的资源类，第二个参数是api端点
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True)