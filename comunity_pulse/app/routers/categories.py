from flask import Blueprint, request,jsonify

from app.schemas.common import MessageResponse
from app.schemas.categories import CategoryBase,CategoryCreate,CategoryUpdate
from pydantic import ValidationError
from app.models import db
from app.models import Category

category_bp = Blueprint('categories',__name__,url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    if categories :
        serialized = [CategoryBase(id=c.id, name=c.name).model_dump() for c in categories ]
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message='No categories found').model_dump()), 200


@category_bp.route('/', methods=['POST'])
def create_category():
    input_data = request.get_json()
    if not input_data:
        return jsonify({"error": "No input data provided"}), 400
    try:
        category_data = CategoryCreate(**input_data)

        existing_category = Category.query.filter_by(name=category_data.name).first()
        if existing_category:
            return jsonify({'error': 'Category already exists'}), 400


        new_category = Category(name=category_data.name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': "Your category was created!"}), 201

    except ValidationError as e:
        error_details = {"error": {error['loc'][0]: error['msg'] for error in e.errors()}}
        return jsonify(error_details), 400


@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    input_data = request.get_json()

    if category:
        try:
            update_data = CategoryUpdate(**input_data)
            category.name = update_data.name
            db.session.commit()
            return jsonify(MessageResponse(message=f"The category with id {id} was updated.").model_dump()), 200
        except ValidationError as e :
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No category with id {id} was found.").model_dump()), 404


@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The category with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No category with id {id} was found.").model_dump()), 404
