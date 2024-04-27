from flask import Flask, request, jsonify
import sqlite3
from middleware.auth import token_required
import jwt
from flask_swagger_ui import get_swaggerui_blueprint

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


@app.route('/addUser', methods=['POST'])
def addUser():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    if user:
        print("user", user)
        token = jwt.encode({'id': str(user[0])}, "secret", algorithm="HS256")
        return jsonify({'token': token})
    else:
        return jsonify({"status": "failed user not found"})


@app.route('/addTask', methods=['POST'])
@token_required
def addTask(id):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    title = data['title']
    content = data['content']
    cur.execute("INSERT INTO tasks (title, content, userId) VALUES (?, ?, ?)", (title, content, id))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/getTasks', methods=['GET'])
@token_required
def getTasks(id):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE userId = ?", (id,))
    tasks = cur.fetchall()
    return jsonify({"tasks": tasks})

@app.route('/deleteTask', methods=['DELETE'])
@token_required
def deleteTask(id):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    title = request.args.get('title')
    cur.execute("DELETE FROM tasks WHERE title = ?", (title,))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/updateTask', methods=['PUT'])
@token_required
def updateTask(id):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    title = data['title']
    content = data['content']
    cur.execute("UPDATE tasks SET content = ? WHERE title = ?", (content, title))
    con.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    