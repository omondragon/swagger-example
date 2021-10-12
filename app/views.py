# views.py

from flask import render_template
from app import app

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
        return jsonify(spec.to_dict())

class ArticleResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        body = fields.Str()
        author = fields.Str()
        create_date = fields.Date()

class ArticleListResponseSchema(Schema):
        article_list = fields.List(fields.Nested(ArticleResponseSchema))

@app.route('/articles')
def article():
    """Get List of Articles
        ---
        get:
            description: Get List of Articles
            responses:
                200:
                    description: Return an article list
                    content:
                        application/json:
                            schema: ArticleListResponseSchema
    """

    articles = [
        {
            'id': 1,
            'title': 'Article one',
            'body': 'Lorem ipsum', 
            'author': 'Gabo',
            'create_date': date(2021,10,4)
        },
        {
            'id': 2,
            'title': 'Article two',
            'body': 'Lorem ipsum', 
            'author': 'Perez', 
            'create_date': date(2021,10,12)
        }
    ]

    return ArticleListResponseSchema().dump({'article_list':articles})

with app.test_request_context():
    spec.path(view=article)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html',base_url='/docs')
    else:
        return send_from_directory('static',path)
