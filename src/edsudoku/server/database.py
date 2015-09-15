from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import as_declarative
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

from edsudoku.server import app

__author__ = 'Eli Daian <elidaian@gmail.com>'

DB_STRING_SIZE = 64
""" String size to use in DB strings. """

engine = create_engine(app.config['DATABASE'], convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))


@as_declarative()
class Base(object):
    """
    Base class for all ORM classes.
    """

    @classmethod
    def query(cls):
        """
        :return: A query object for this class.
        :rtype: :class:`sqlalchemy.orm.query.Query`
        """
        return db_session.query(cls)

    @classmethod
    def get_by_id(cls, id):
        """
        :return: The object of the row with the given ID, or ``None`` if user with this ID does not exist.
        :rtype: cls
        """
        return cls.query().filter_by(id=id).first()

    def add(self):
        """
        Add the current object to the session.
        """
        db_session.add(self)

    def delete(self):
        """
        Delete the current object from the session.
        """
        db_session.delete(self)


def commit():
    """
    Commit current state to the DB.
    """
    db_session.commit()


def rollback():
    """
    Roll back the session state.
    """
    db_session.rollback()
