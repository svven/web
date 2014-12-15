# -*- coding: utf-8 -*-

from flask import Markup
from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, BooleanField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, Length

from database.twitter.models import User
from database import db
from ..config import (USERNAME_LEN_MAX, USERNAME_LEN_MIN)


class LoginForm(Form):
    next = HiddenField()
    login = StringField(u'Username or email', [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class SignupForm(Form):
    next = HiddenField()
    screen_name = StringField(u'Choose your username', [DataRequired(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
                              description=u"Don't worry. you can change it later.")
    name = StringField(u'Please provide your name', [DataRequired(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
                       description=u"First name and surname.")
    email = StringField(u'And email please', [DataRequired(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    agree = BooleanField(u'Agree to the ' +
                         Markup('<a target="blank" href="/terms">Terms of Service</a>'), [DataRequired()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        s = db.Session()
        if s.query(User).filter_by(screen_name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

