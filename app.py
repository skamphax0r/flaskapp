#imports: 
import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'SECRETKEY'
api = Api(app)


jwt = JWT(app, authenticate, identity) #creates /auth

    
#add resource to api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

#run the app
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '8080')))