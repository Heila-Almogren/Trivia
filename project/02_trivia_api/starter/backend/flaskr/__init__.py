import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import babel
import dateutil.parser
import json
from flask_migrate import Migrate
import datetime
# from posix import abort
from enum import Enum
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case


from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    app.debug = True
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        
        """
        Returns:
            the list of all categories
        """

        categories = Category.query.all()
        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories,

        })

    @app.route('/questions', methods=['GET'])
    def questions():
        
        """
        Returns:
            the list of all questions
        """

        page = request.args.get('page', 1, type=int)
        start = (page-1) * 10
        end = start + 10
        questions = Question.query.all()
        formatted_questions = [question.format()
                               for question in questions]
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'totalQuestions': len(formatted_questions),
            'categories': {category.id: category.type
                           for category in Category.query.all()}
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        
        """
        Returns:
            the result of deleting a question
        Args:
            question id
        """

        try:
            ques = Question.query.get(question_id)
            db.session.delete(ques)
            db.session.commit()
            return jsonify({
                'success': True,
            })

        except Exception as e:
            print(e)
            error = True
            db.session.rollback()
        finally:
            db.session.close()
            return None

    @app.route('/questions/create', methods=['POST'])
    def create_question():
        
        """
        Returns:
            the result of creating a question
        """

        try:
            question = request.json['question']
            answer = request.json['answer']
            difficulty = request.json['difficulty']
            category = request.json['category']

            nQuestion = Question(
                question=question, answer=answer, category=category, difficulty=difficulty, )

            db.session.add(nQuestion)

            db.session.commit()

            page = request.args.get('page', 1, type=int)
            start = (page-1) * 10
            end = start + 10
            questions = Question.query.all()
            formatted_questions = [question.format()
                                   for question in questions]
            return jsonify({
                'success': True,
            })

        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    @app.route('/questions', methods=['POST'])
    def search_questions():
        
        """
        Returns:
            the result of searching for a questions
        """

        term = request.json['searchTerm']

        print("term is ")
        page = request.args.get('page', 1, type=int)
        start = (page-1) * 10
        end = start + 10
        questions = Question.query.filter(Question.question.ilike(f'%{term}%'))
        formatted_questions = [question.format()
                               for question in questions]
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'totalQuestions': len(formatted_questions),
            'categories': {category.id: category.type
                           for category in Category.query.all()}
        })

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def Questions_of_cat(category_id):
        
        """

        Returns:
            Shows list of questions based ona a specific category

        Args:
            category id

        """

        page = request.args.get('page', 1, type=int)
        start = (page-1) * 10
        end = start + 10
        questions = Question.query.filter(Question.category == category_id)
        formatted_questions = [question.format()
                               for question in questions]
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'totalQuestions': len(formatted_questions),
            'categories': {category.id: category.type
                           for category in Category.query.all()}
        })

    @app.route('/quizzes', methods=['POST'])
    def createquiz():
        
        """

        Returns:
            returns a new question in the quiz such that it\'s not repeated

        """

        quiz_category = request.json['quiz_category']

        allQuestions = Question.query.filter(
            Question.category == quiz_category['id']).all()

        possibleQuestions = [q.id for q in allQuestions]
        print('possible questions: ', possibleQuestions)
        previousQuestions = request.json['previous_questions']
        print('previous questions: ', previousQuestions)

        possibilities = len(possibleQuestions)
        previous = len(previousQuestions)

        if possibilities == previous:
            return jsonify({
                'question': None
            })

        for possibility in possibleQuestions:
            if not possibility in previousQuestions:
                print('found: ', possibility)
                break

        currentQuestion = Question.query.get(possibility)
        print('current: ', currentQuestion)

        return jsonify({
            'question': {'id': currentQuestion.id, 'question': currentQuestion.question, 'answer': currentQuestion.answer, 'difficulty': currentQuestion.difficulty, 'category': currentQuestion.category},
        })

    @app.errorhandler(404)
    def not_found(error):
        
        """

        returns:
            handling for 404 (Not found) Error

        """

        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        
        """

        returns:
            handling for 422 (unprocessable) Error

        """

        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app


#hope #hardwork & always wide #smile :D