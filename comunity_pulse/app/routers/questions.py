from flask import Blueprint, request,jsonify
from pydantic import ValidationError


from app.models.question import Question
from app.models.category import Category
from app.schemas.questions import MessageResponse, QuestionCreate,QuestionSchema
from app.models import db

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    serialized = [QuestionSchema(id=q.id, text=q.text, category=q.category.name).model_dump()for q in questions]

    if questions:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return  jsonify(MessageResponse(message="No questions found").model_dump()), 200

@questions_bp.route('/', methods=['POST'])
def create_question():

    input_data = request.get_json()
    try:
        question_data = QuestionCreate(**input_data)
        category = db.session.query(Category).filter_by(name=question_data.category).first()
        if not category:
            category = Category(name=question_data.category)
            db.session.add(category)
            db.session.commit()
        question = Question(text=question_data.text,category_id=category.id)
        db.session.add(question)
        db.session.commit()
    except ValidationError as e :
        return jsonify({"error": e.errors}), 400

    return jsonify({'message':"Your questions was created!"}), 200

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""
    return f"Детали вопроса {id}"

@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление конкретного вопроса по его ID."""
    return f"Вопрос {id} обновлен"

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    return f"Вопрос {id} удален"
