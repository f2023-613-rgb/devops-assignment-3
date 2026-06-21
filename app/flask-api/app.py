from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'mysql'),
        user=os.environ.get('DB_USER', 'flaskuser'),
        password=os.environ.get('DB_PASSWORD', 'flaskpass'),
        database=os.environ.get('DB_NAME', 'flaskdb')
    )

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"service": "flask-api", "status": "healthy"}), 200

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items;')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (name, description))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/items', methods=['GET', 'POST'])
def api_items():
    if request.method == 'POST':
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (data['name'], data['description']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Item added successfully!"}), 201
    else:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM items;')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(items), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
