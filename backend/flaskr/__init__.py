import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # Any resources under / can be accessed by any origins.
  cors = CORS(app, resources={r"/*": {"origins": "*"}})


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)

    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success': True, 
      'categories': formatted_categories
    })


  def paginate_questions(request, selection):
    # Pagination
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    return selection[start:end]


  @app.route('/questions', methods=['GET'])
  def get_questions():
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    selection = Question.query.order_by(Question.id).all()
    current_questions = [question.format() for question in paginate_questions(request, selection)]
    if len(current_questions) == 0:
      abort(404)

    current_category = []
    categories = [category.format() for category in Category.query.all()]
    
    return jsonify({
      'success': True, 
      'questions': current_questions, 
      'total_questions': len(selection), 
      'current_category': current_category, 
      'categories': categories
    })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None:
      abort(404)

    else:
      try: 
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_questions = [question.format() for question in paginate_questions(request, selection)]

        return jsonify({
          'success': True, 
          'deleted': question_id, 
          'questions': current_questions, 
          'total_questions': len(Question.query.all())
        })

      except:
        abort(422)


  @app.route('/questions', methods=['POST'])
  def create_question():
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  

    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    body = request.get_json()

    # print('getting values..')
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search_term = body.get('search_term', None)
    # print('converting types..')
    if new_difficulty:
      new_difficulty = int(new_difficulty)

    try:
      if search_term:
        # print('searching.. {}'.format(search_term))
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
        # print('len(selection):', len(selection))
        # print('paginating..')
        current_questions = [question.format() for question in paginate_questions(request, selection)]

        # print('return')
        return jsonify({
          'success': True, 
          'questions': current_questions, 
          'total_questions': len(selection)
        })

      else:
        # print('creating a question instance..')
        question = Question(
          question=new_question, 
          answer=new_answer, 
          category=new_category, 
          difficulty=new_difficulty
        )
        # print('inserting the question instance..')
        question.insert()
        print('inserted.')

        selection = Question.query.order_by(Question.id).all()
        current_questions = [question.format() for question in paginate_questions(request, selection)]

        return jsonify({
          'success': True, 
          'created': question.id, 
          'questions': current_questions, 
          'total_questions': len(Question.query.all())
        })

    except:
      abort(422)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    current_questions = [question.format() for question in paginate_questions(request, selection)]
    if len(current_questions) == 0:
      abort(404)

    current_category = Category.query.get(category_id)
    # print('category:', current_category)
    if current_category is None:
      abort(404)

    return jsonify({
      'success': True, 
      'questions': current_questions, 
      'total_questions': len(selection), 
      'current_category': current_category.format()
    })









  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405, 
      "message": "method not allowed"
    }), 405


  
  return app

    