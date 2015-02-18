"""
News blueprint.
"""
from flask import Blueprint, render_template

from sqlalchemy.orm import joinedload, contains_eager

from database.models import *

news = Blueprint('news', __name__)
