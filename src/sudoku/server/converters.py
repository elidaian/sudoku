from werkzeug.routing import BaseConverter, ValidationError

__author__ = "Eli Daian <elidaian@gmail.com>"


class BooleanConverter(BaseConverter):
    """
    Converter of boolean expressions in the URL.

    * ``False`` will be converted to ``false``.
    * ``True`` will be converted to ``true``.

    Any other value will cause an error.
    """

    regex = "(?:true|false)"

    def to_python(self, value):
        """
        Get a value from the URL, and convert it to a Python boolean.

        :param value: The URL value.
        :type value: str
        :return: The Python conversion.
        :rtype: bool
        """

        if value == "true":
            return True
        elif value == "false":
            return False
        raise ValidationError()

    def to_url(self, value):
        """
        Get a Python boolean and convert it to a URL form.

        :param value: The Python value.
        :type value: bool
        :return: The URL conversion.
        :rtype: str
        """
        return "true" if value else "false"
