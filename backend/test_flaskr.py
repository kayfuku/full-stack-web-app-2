import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "trivia_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

    self.new_question = {
      'question': 'q1',
      'answer': 'a1',
      'category': '1', 
      'difficulty': 1
    }


  def tearDown(self):
    """Executed after reach test"""
    pass


  """
  TODO
  Write at least one test for each test for successful operation and for expected errors.
  """
  def test_get_paginated_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_questions'])
    self.assertTrue(len(data['questions']))


  def test_get_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['categories']))


  def test_404_sent_requesting_invalid_page(self):
    res = self.client().get('/questions?page=1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')


  # def test_delete_question(self):
  #   res = self.client().delete('/questions/4')
  #   data = json.loads(res.data)

  #   question = Question.query.filter(Question.id == 1).one_or_none()

  #   self.assertEqual(res.status_code, 200)
  #   self.assertEqual(data['success'], True)
  #   self.assertEqual(data['deleted'], 4)
  #   self.assertTrue(data['total_questions'])
  #   self.assertTrue(len(data['questions']))
  #   self.assertEqual(question, None)


  # def test_create_new_question(self):
  #   res = self.client().post('/questions', json=self.new_question)
  #   data = json.loads(res.data)

  #   self.assertEqual(res.status_code, 200)
  #   self.assertEqual(data['success'], True)
  #   self.assertTrue(data['created'])
  #   self.assertTrue(len(data['questions']))


  def test_get_question_search_with_results(self):
    res = self.client().post('/questions', json={'search_term': 'what'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_questions'])
    self.assertEqual(len(data['questions']), 7)


  def test_get_question_search_without_results(self):
    res = self.client().post('/questions', json={'search_term': 'xxx'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], 0)
    self.assertEqual(len(data['questions']), 0)






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()