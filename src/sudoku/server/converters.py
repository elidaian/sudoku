from itertools import imap
from werkzeug.routing import BaseConverter, ValidationError

__author__ = 'Eli Daian <elidaian@gmail.com>'


class BooleanConverter(BaseConverter):
    """
    Converter of boolean expressions in the URL.

    * ``False`` will be converted to ``false``.
    * ``True`` will be converted to ``true``.

    Any other value will cause an error.
    """

    regex = '(?:true|false)'

    def to_python(self, value):
        """
        Get a value from the URL, and convert it to a Python boolean.

        :param value: The URL value.
        :type value: str
        :return: The Python conversion.
        :rtype: bool
        """

        if value == 'true':
            return True
        elif value == 'false':
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
        return 'true' if value else 'false'


class IntegersListConverter(BaseConverter):
    """
    Convert a list of ints from the URL.

    For example, the list [1, 2, 3] will be converted to '1/2/3'.
    """

    regex = r'[^/]?(/?\d+)+'

    def to_python(self, value):
        """
        Convert a list from URL to Python.

        :param value: The URL list.
        :type value: str
        :return: The Python list.
        :rtype: list of ints
        """
        return map(int, value.split('/'))

    def to_url(self, value):
        """
        Convert a list from python to url.

        :param value: The Python list.
        :type value: list of ints
        :return: The URL list.
        :rtype: str
        """
        return '/'.join(imap(str, value))
