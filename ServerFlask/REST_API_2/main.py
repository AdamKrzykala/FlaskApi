# This Python file uses the following encoding: utf-8
import self as self
from flask import Flask, url_for, make_response, redirect, request, jsonify, Blueprint
method = ''
done = False


class Server(Flask):
    admin = Blueprint('admin', __name__)
    user = Blueprint('user', __name__)
    app = Flask(__name__)

    def __init__(self):
        super(Server, self).__init__(__name__)
        self.app.add_url_rule('/index1', view_func=self.index1)
        self.app.add_url_rule('/index2', view_func=self.index2)
        self.app.add_url_rule('/index3', endpoint="index3")
        self.app.register_blueprint(self.admin, url_prefix='/admin')
        self.app.register_blueprint(self.user, url_prefix='/user')

    @staticmethod
    @admin.route('/greeting')
    def greeting():
        return 'Hello, administrative user!'

    @staticmethod
    @user.route('/greeting')
    def greeting():
        return 'Hello, lowly normal user!'

    @staticmethod
    @app.before_request
    def func_before():
        global method
        global done
        method = request.method
        done = False

    @staticmethod
    @app.errorhandler(404)
    def not_found(errno):
        return f"NOT FOUND {errno} \n"

    @staticmethod
    @app.route('/api/auth', methods=['POST', 'GET'])
    def auth():
        json_data = request.get_json()
        email = json_data['email']
        password = json_data['password']
        return jsonify(email, password, method, done)

    @staticmethod
    @app.route('/index')
    def index():
        method = request.method
        args = request.args
        data = request.data
        savedData = request.form
        headers = request.headers
        return redirect('/index1')

    @staticmethod
    def index1():
        return redirect(url_for('index2'))

    @staticmethod
    def index2():
        return jsonify(method)

    @staticmethod
    @app.endpoint("index3")
    def index3EndPoint():
        global done
        done = True
        return jsonify(done)

    @staticmethod
    @app.route('/sayHiToAdministrator')
    def sayHiAdmin():
        return redirect(url_for('admin.greeting'))

    @staticmethod
    @app.route('/sayHiToUser')
    def sayHiUser():
        return redirect(url_for('user.greeting'))

    def testClass(self):
        with self.app.test_client() as c:
            rv = c.post('/api/auth', json={
                'email': 'flask@example.com', 'password': 'secret'
            })
            jsonData = rv.get_json()
            print(jsonData)
            rv = c.get('/index2')
            jsonData = rv.get_json()
            print(jsonData)

    def start(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    server = Server()
    server.testClass()
    server.start()

