import importlib.util
import logging

# Standard library imports
import os
from datetime import timedelta
from logging.handlers import TimedRotatingFileHandler

import rsa
from flask import Flask, has_request_context, request
from flask_wtf.csrf import CSRFProtect

from .config import DevelopmentConfig


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    csrf = CSRFProtect()
    csrf.init_app(app)
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None
            return super().format(record)

    formatter = RequestFormatter(
        "{'TIME':%(asctime)s,'ADDRESS':'%(remote_addr)s','URL': '%(url)s','TYPE':'%(levelname)s','MODULE':'%(module)s','MSG':{%(message)s}}"
    )

    register_blueprints(app, "src")

    app.config.from_object(config)
    app.config["RSA_PUBLIC"], app.config["RSA_PRIVATE"] = rsa.newkeys(600)
    print(f'ENV is set to: {app.config["ENV"]}')
    print(app.config)

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=5)

    handler = TimedRotatingFileHandler(
        app.config["LOG_FILE"], when="midnight", interval=1, encoding="utf8"
    )
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return app


def register_blueprints(app, dir):
    try:
        lst = os.listdir("app/" + dir)
    except OSError:
        print("NO SE PUDIERON CARGAR LAS BLUEPRINTS")
    else:
        for name_route in lst:
            if name_route != "__pycache__":
                name_class = name_route.split(".py")[0]
                module = importlib.import_module("app." + dir + "." + name_class)
                app.register_blueprint(getattr(module, name_class))
