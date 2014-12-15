# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField,
                     SubmitField)
from flask.ext.login import current_user

from database.twitter.models import User


class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    # Don't use the same name as model because we are going to use populate_obj().
    submit = SubmitField(u'Save')

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError("Please pick another name.")
