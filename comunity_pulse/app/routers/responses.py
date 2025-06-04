from flask import Blueprint, request

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')

@responses_bp.route('/', methods=['GET'])
def get_responses():
    """Получение статистики ответов."""
    return "Статистика всех ответов"

@responses_bp.route('/', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос."""
    return "Ответ добавлен"
