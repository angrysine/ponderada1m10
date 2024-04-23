from flask import Flask, request, jsonify
import sqlite3
import jwt
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
SWAGGER_URL="/swagger"
API_URL="/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)






app = Flask(__name__)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open("swagger.json") as f:
        data = f.read()
    return data

# Decorator to check if token is valid
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # Get token from query string

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = data['id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/addUser', methods=['POST'])
@token_required
def addUser():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    encoded_jwt = jwt.encode(password, "secret", algorithm="HS256")
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encoded_jwt))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/getUserId', methods=['GET'])
@token_required
def getUserId():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = request.args.get('username')
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    userId = cur.fetchone()[0]
    return jsonify({"userId": userId})

@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    encoded_jwt = jwt.encode(password, "secret", algorithm="HS256")
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, encoded_jwt))
    user = cur.fetchone()
    if user:
        token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({"status": "failed user not found"})


@app.route('/addTask', methods=['POST'])
@token_required
def addTask():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    title = data['title']
    content = data['content']
    userId = data['userId']
    cur.execute("INSERT INTO tasks (title, content, userId) VALUES (?, ?, ?)", (title, content, userId))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/getTasks', methods=['GET'])
@token_required
def getTasks():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    userId = request.args.get('userId')
    cur.execute("SELECT * FROM tasks WHERE userId = ?", (userId,))
    tasks = cur.fetchall()
    return jsonify({"tasks": tasks})

@app.route('/deleteTask', methods=['DELETE'])
@token_required
def deleteTask():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    title = request.args.get('title')
    cur.execute("DELETE FROM tasks WHERE title = ?", (title,))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/updateTask', methods=['PUT'])
@token_required
def updateTask():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    title = data['title']
    content = data['content']
    cur.execute("UPDATE tasks SET content = ? WHERE title = ?", (content, title))
    con.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    