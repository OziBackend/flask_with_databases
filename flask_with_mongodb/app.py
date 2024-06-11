from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['myDatabase']
collection = db['mycollection']

# Helper function to format MongoDB documents
def format_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Create (POST)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Read (GET)
@app.route('/items', methods=['GET'])
def get_items():
    items = collection.find()
    return jsonify([format_document(item) for item in items]), 200

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = collection.find_one({'_id': ObjectId(id)})
    if item:
        return jsonify(format_document(item)), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# Update (PUT)
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Item updated'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

# Delete (DELETE)
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Item deleted'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
