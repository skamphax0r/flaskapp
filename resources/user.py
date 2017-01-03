import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required=True,
        help="cannot be blank"
    )
    parser.add_argument('password',
        type = str,
        required=True,
        help="cannot be blank"
    )
        
    def post(self):
        data = UserRegister.parser.parse_args()
        ## Does user already exist? 
        if UserModel.find_by_username(data['username']):
            return {"Message": "user already exists"}, 400
        else:
            user = UserModel(**data)
            user.save_to_db()
            
            return {"Message": "user created successfully"}, 201
            