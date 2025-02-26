from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return length of data"""
    if data:
        return data , 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic.get("id") == id:
            return  pic  , 200 # Return the matched picture
        
    return jsonify({"Message": f"picture with id {pic['id']} already not found"}), 404
      


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
        # Extract picture data from request body
    picture = request.get_json()

    # Check if picture with the same ID already exists
    for pic in data:
        if pic["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append new picture to data list
    data.append(picture)  # Append new picture
    with open(json_url, "w", encoding="utf-8") as file: 
        json.dump(data, file, indent=4)  # Save back to JSON file
    return picture, 201


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):

    # get data from the json body
    picture_in = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201

    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204

    return {"message": "picture not found"}, 404
