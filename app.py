# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'id': item.id, 'name': item.name} for item in items]
    return jsonify(items_list)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
