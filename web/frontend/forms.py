# -*- coding: utf-8 -*-

from flask import Markup
from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, BooleanField, StringField,
                     SubmitField)
from wtforms.validators import Required, Length

from ..auth.models import User
from ..config import (USERNAME_LEN_MAX, USERNAME_LEN_MIN)


class LoginForm(Form):
	next = HiddenField()
	login = StringField(u'Username or email', [Required()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Sign in')


class SignupForm(Form):
	next = HiddenField()
	screen_name = StringField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
	                          description=u"Don't worry. you can change it later.")
	agree = BooleanField(u'Agree to the ' +
	                     Markup('<a target="blank" href="/terms">Terms of Service</a>'), [Required()])
	submit = SubmitField('Sign up')

	def validate_name(self, field):
		if User.query.filter_by(name=field.data).first() is not None:
			raise ValidationError(u'This username is taken')

