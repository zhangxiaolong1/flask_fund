# -*- coding: UTF-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from configs.config import current_config

engine = create_engine(current_config.SQLALCHEMY_DATABASE_URI, echo=False)
db = SQLAlchemy()


