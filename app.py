from flask import Flask, request, jsonify
import sqlite3
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


# encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")



app = Flask(__name__)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open("swagger.json") as f:
        data = f.read()
    return data


@app.route('/addUser', methods=['POST'])
def api():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/getUserId', methods=['GET'])
def getUserId():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = request.args.get('username')
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    userId = cur.fetchone()[0]
    return jsonify({"userId": userId})

@app.route('/addTask', methods=['POST'])
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
def getTasks():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    userId = request.args.get('userId')
    cur.execute("SELECT * FROM tasks WHERE userId = ?", (userId,))
    tasks = cur.fetchall()
    return jsonify({"tasks": tasks})

@app.route('/deleteTask', methods=['DELETE'])
def deleteTask():
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    title = request.args.get('title')
    cur.execute("DELETE FROM tasks WHERE title = ?", (title,))
    con.commit()
    return jsonify({"status": "success"})

@app.route('/updateTask', methods=['PUT'])
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
    