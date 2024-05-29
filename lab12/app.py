from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    user_id = data['user_id']
    title = data['title']
    content = data['content']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    content = data['content']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, user_id, content))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

if __name__ == '__main__':
    app.run(debug=True)
