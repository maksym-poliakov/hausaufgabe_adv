from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models.response import Response
from app.schemas.common import MessageResponse
from app.schemas.responses import ResponseCreate, ResponseSchema, ResponseUpdate
from app.models import db, Statistic

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')


@responses_bp.route('/', methods=['GET'])
def get_responses():
    responses = Response.query.all()
    serialized = [ResponseSchema(question_text=r.question.text, is_agree=r.is_agree).model_dump() for r in responses]

    if responses:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No responses found").model_dump()), 404


@responses_bp.route('/', methods=['POST'])
def create_response():
    input_data = request.get_json()
    if not input_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        response_data = ResponseCreate(**input_data)
        response = Response(question_id=response_data.question_id, is_agree=response_data.is_agree)
        db.session.add(response)
        db.session.commit()

        # Обновление статистики
        statistic = Statistic.query.get(response.question_id)
        if statistic:
            if response.is_agree:
                statistic.agree_count += 1
            else:
                statistic.disagree_count += 1
            db.session.commit()
        else:
            new_stat = Statistic(question_id=response.question_id, agree_count=1 if response.is_agree else 0,
                                 disagree_count=1 if not response.is_agree else 0)
            db.session.add(new_stat)
            db.session.commit()

        return jsonify(MessageResponse(message="Your response was created!").model_dump()), 201

    except ValidationError as e:
        return jsonify({'error': {error['loc'][0]: error['msg'] for error in e.errors()}}), 400
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@responses_bp.route('/<int:id>', methods=['GET'])
def get_response(id):
    response = Response.query.get(id)

    if response:
        return jsonify(MessageResponse(message=ResponseSchema(question_text=response.question.text,
                                                              is_agree=response.is_agree).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump())


@responses_bp.route('/<int:id>', methods=['PUT'])
def update_response(id):
    response = Response.query.get(id)
    input_data = request.get_json()
    if not input_data:
        return jsonify({"error": "No input data provided"}), 400

    if response:
        try:
            updated_data = ResponseUpdate(**input_data)
            response.is_agree = updated_data.is_agree
            response.question_id = updated_data.question_id
            db.session.commit()

            # Обновление статистики
            statistic = Statistic.query.get(response.question_id)
            if statistic:
                old_responses = Response.query.filter_by(question_id=response.question_id).all()
                statistic.agree_count = sum(1 for r in old_responses if r.is_agree)
                statistic.disagree_count = sum(1 for r in old_responses if not r.is_agree)
                db.session.commit()

            return jsonify(MessageResponse(message=f"The response with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': {error['loc'][0]: error['msg'] for error in e.errors()}}), 400
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404


@responses_bp.route('/<int:id>', methods=['DELETE'])
def delete_response(id):
    response = Response.query.get(id)
    if response:
        db.session.delete(response)
        db.session.commit()

        statistic = Statistic.query.get(response.question_id)
        if statistic:
            old_responses = Response.query.filter_by(question_id=response.question_id).all()
            statistic.agree_count = sum(1 for r in old_responses if r.is_agree)
            statistic.disagree_count = sum(1 for r in old_responses if not r.is_agree)
            db.session.commit()

        return jsonify(MessageResponse(message=f"The response with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404


@responses_bp.route('/stat', methods=['GET'])
def get_statistic():

    statistics = Statistic.query.all()
    results = [
        {
            "question_id": stat.question_id,
            "agree_count": stat.agree_count,
            "disagree_count": stat.disagree_count
        }
        for stat in statistics
    ]
    return jsonify(results), 200