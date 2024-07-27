from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


    db.init_app(app)
    jwt.init_app(app)
    

    @app.route('/test', methods=['GET'])
    def test():
        return {"message": "Test route working"}

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
       
        return response

    with app.app_context():
        from resources.user import UserRegister, UserLogin
        from flask_restful import Api

        api = Api(app)
        api.add_resource(UserRegister, '/register')
        api.add_resource(UserLogin, '/login')

        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
