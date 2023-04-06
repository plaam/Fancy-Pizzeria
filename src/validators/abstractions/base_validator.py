import re
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from abc import ABC, abstractmethod

from flask import render_template


class BaseValidator(ABC):
    def __init__(self, data, method):
        self.data = data
        self.method = method
        self.validation_methods = {
            'POST': self.validate_create,
            'PUT': self.validate_update
        }

    def validate(self):
        validate_method = self.validation_methods.get(self.method)
        if validate_method:
            return validate_method()

        return {'error': 'Validation error: Invalid HTTP request method'}, 400

    @abstractmethod
    def validate_create(self):
        pass

    @abstractmethod
    def validate_update(self):
        pass

    @staticmethod
    def validate_username(username):
        if not username:
            error_message = 'Validation error: Username is required'
            return render_template('signup.html', error_message=error_message)

        if len(username) < 4 or len(username) > 12:
            error_message = 'Validation error: Username must be between 4 and 12 characters'
            return render_template('signup.html', error_message=error_message)

        return None, None

    @staticmethod
    def validate_password(password):
        if not password:
            error_message = 'Validation error: Password is required'
            return render_template('signup.html', error_message=error_message)

        if not re.match(r'^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!#%]*[!#%])[A-Za-z0-9!#%]{6,32}$', password):
            error_message = 'Validation error: Password must contain at least one lowercase letter, one uppercase ' \
                            'letter, one digit, and one special character (!, #, or %) and be between 6 and 32 ' \
                            'characters'
            return render_template('signup.html', error_message=error_message)

        return None, None
