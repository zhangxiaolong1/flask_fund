# -*- coding: utf-8 -*-
import time
from flask import request
from app import create_app
from configs.application import app
from configs.db_config import db

app = create_app(app)


@app.before_first_request
def base_init():
    db.create_all()
    db.init_app(app)
    db.create_all()


@app.before_request
def before_request():
    request.cache_triggers = []
    request.start_time = time.time()
    request.sxtimer_stack = ['-']


@app.after_request
def after_request(response):
    db.session.remove()

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,VIEW'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type, Mall-Token, User-Token, Admin-Token'

    return response


def health_check():
    return "pong!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
