from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {"message": "A users with the same username exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created successfully"}, 201
