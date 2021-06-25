from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # TODO: Set up CORS

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # get all available categories
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.type).all()

        if not categories:
            abort(404)

        return jsonify({
            'success': True,
            'categories': [category.format() for category in categories],
        })

    # get all available questions
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': None,
            'categories': [category.format() for category in categories]
        })

    # DELETE question using a question ID
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True
            })

        except:
            abort(422)

    # Create a new question
    # Search questions
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        query = body.get('searchTerm', None)

        if query is not None:
            try:
                matches = Question.query.filter(Question.question.ilike('%' + query + '%')).all()
                current_questions = paginate_questions(request, matches)

                return jsonify({
                    'questions': current_questions,
                    'totalQuestions': len(matches),
                    'currentCategory': None
                })
            except:
                abort(422)

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        if new_question is None or new_answer is None or new_difficulty is None or new_category is None:
            abort(400)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty,
                                category=new_category)
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    # Get questions based on category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()

            if not questions:
                abort(404)

            current_questions = paginate_questions(request, questions)
            category = Category.query.get(category_id)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': category.type
            })

        except:
            abort(422)

    # Get questions to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()
            if not ('quiz_category' and 'previous_questions' in body):
                abort(422)
            quiz_category = body.get('quiz_category')['id']
            previous_questions = body.get('previous_questions')
            if quiz_category != 0:
                new_question = Question.query.filter_by(
                    category=quiz_category
                ).filter(Question.id.not_in(previous_questions)).all()
            else:
                new_question = Question.query.filter(
                    Question.id.not_in(previous_questions)
                ).all()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'question': random.choice(new_question).format() if new_question else None,
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
