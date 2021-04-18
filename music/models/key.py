from django.core import exceptions
from django.db import models

from utils import key


class KeyField(models.CharField):
    """
    Implement a field that only holds value that represents valid music key.
    The key is stored in the openkey music format
    """

    description = "A music key"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 3
        super().__init__(*args, **kwargs)
        self.key = None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    @classmethod
    def validate_key(cls, value):
        """
        Validates the key by trying to find it in the 3 supported music notation
        """
        if value is None:
            return None
        elif value in set(k.value for k in key.OpenKey):
            return key.OpenKey(value)
        elif value in set(k.value for k in key.CamelotKey):
            return key.camelotKeyToOpenKey[key.CamelotKey(value)]
        elif value in set(k.value for k in key.MusicKey):
            return key.musicKeyToOpenKey[key.MusicKey(value)]
        else:
            raise exceptions.ValidationError("Invalid music key : {}".format(value))

    def to_python(self, value):
        if isinstance(value, key.OpenKey):
            return value
        if value is None:
            return value

        return KeyField.validate_key(value)

    # Convert a python object (key.OpenKey) to a database value (str)
    def get_prep_value(self, value):
        if isinstance(value, key.OpenKey):
            return value.value
        elif isinstance(value, key.CamelotKey):
            return key.camelotKeyToOpenKey[value].value
        elif isinstance(value, key.MusicKey):
            return key.musicKeyToOpenKey[value].value
        elif value is None:
            return value
        elif isinstance(value, str):
            return self.validate_key(value)
        else:
            raise exceptions.ValidationError("Invalid music key : {}".format(value))

    # Convert a database value (str) to python a value (key.OpenKey)
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return KeyField.validate_key(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.validate_key(self.get_prep_value(value))