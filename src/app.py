"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

john = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

jane = {
    "first_name": "Jane" ,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def the_only_one(id):
    
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def a_new_member():
    request_body = request.json
    if "first_name" not in request_body or request_body["first_name"] is None or request_body["first_name"] == "":
        return jsonify({"message": "first_name is required"}), 400
    
    elif "age" not in request_body or request_body["age"] is None or request_body["age"] == "":
        return jsonify({"message": "age is required"})
    
    elif "lucky_numbers" not in request_body or request_body["lucky_numbers"] is None or request_body["lucky_numbers"] == "":
        return jsonify({"message": "lusky_numbers is required"})
    
    else:
        the_member= jackson_family.add_member(request_body)
        return jsonify(the_member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_this_member(id):
    
    jackson_family.delete_member(id)    
    return jsonify({'done': True}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
