# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from wtforms import (ValidationError, TextField, HiddenField,
                     PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
                     FileField)
from wtforms.validators import (Required, Length, EqualTo, Email, NumberRange,
                                URL, AnyOf, Optional)
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, AGE_MIN, AGE_MAX
from ..utils import SEX_TYPE


class ProfileForm(Form):
	multipart = True
	next = HiddenField()
	email = EmailField(u'Email', [Required(), Email()])
	# Don't use the same name as model because we are going to use populate_obj().
	avatar_file = FileField(u"Avatar", [Optional()])
	sex_code = RadioField(u"Sex", [AnyOf([str(val) for val in SEX_TYPE.keys()])],
	                      choices=[(str(val), label) for val, label in SEX_TYPE.items()])
	age = IntegerField(u'Age', [Optional(), NumberRange(AGE_MIN, AGE_MAX)])
	phone = TelField(u'Phone', [Length(max=64)])
	url = URLField(u'URL', [Optional(), URL()])
	location = TextField(u'Location', [Length(max=64)])
	bio = TextAreaField(u'Bio', [Length(max=1024)])
	submit = SubmitField(u'Save')

	def validate_name(form, field):
		user = User.get_by_id(current_user.id)
		if not user.check_name(field.data):
			raise ValidationError("Please pick another name.")


class PasswordForm(Form):
	next = HiddenField()
	password = PasswordField('Current password', [Required()])
	new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
	password_again = PasswordField('Password again',
	                               [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
	submit = SubmitField(u'Save')

	def validate_password(form, field):
		user = User.get_by_id(current_user.id)
		if not user.check_password(field.data):
			raise ValidationError("Password is wrong.")
