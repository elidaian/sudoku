WSGI Application
****************

Before getting started with the WSGI application, make sure you have an :doc:`installed </installation>` version of
``edsudoku``.

Sample Application
==================

A complete WSGI application could be:

.. code-block:: python

    from edsudoku.server import app as application

And that's it!

Configuring the WSGI Application
================================

The WSGI ``edsudoku`` application reads its configuration from a file named ``sudoku.cfg``.
Currently, this file is not supplied with the package distribution of ``edsudoku``.

A sample file would look like:

.. code-block:: python

    from os.path import dirname, join

    # DB connection string, to be passed to SQLAlchemy
    DATABASE = 'sqlite:///{}'.format(join(dirname(__file__), 'sudoku.db'))

    # Set this flag to True in order to display Flask's debug page when
    # internal server errors occur.
    DEBUG = True

    # Secret key (generated using os.urandom). Regenerate for your configuration
    SECRET_KEY = '\x11\x96<\xdb\xd3$/\xc7\x82\xb3\xf7Zj\xe0n\\'

In newer versions, this file will be supplied with ``edsudoku`` package installation.

Initializing the DB
===================

After configuring the application, the DB can be initialized simply using the command ``edsudoku-init-db``.
This command is responsible for creating an empty DB, with a single root user configured in it.

A *root user* is a user that have the most privileges in the website. It has permissions to create boards, view boards
(even of other users) and manage the users in the website (registering new users, editing and deleting existing users).
With a root user configured, the website can be used, and any user can be registered. It is important to configure a
root user, since the website is not usable without it.

The signature of the ``edsudoku-init-db`` command is as follows::

    usage: init_db.py [-h] [-u USERNAME] [-p PASSWORD] [-d]

    Initialize an empty DB

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --user USERNAME
                            Root user name
      -p PASSWORD, --password PASSWORD
                            Root user password
      -d, --drop-old        Use for dropping all information in the DB

This command creates an empty DB, with the given root user configured. The root user name is the given username, or
the operating system username (as obtained by :func:`getpass.getuser`). The password could be passed as an argument to
``edsudoku-init-db``, or could be given to the process in the standard input.

If the ``-d`` option is passed, then all information in the DB will be dropped (deleted), and a new DB will replace the
existing one.

The DB is accessed by using the WSGI application configuration file, so don't forger to configure the DB connection
string before initializing the DB.

:Tip: It is more recommended that the password will not be passed as a command line argument if possible, in order to
    maintain it as secure as possible.

The DB will never store your password in plaintext. It will be hashed using the `SHA-512
<https://en.wikipedia.org/wiki/SHA-2>`_ algorithm, and 16 bytes of salt will be added to the password.

Generating PDF Boards
=====================

PDF board generation is done using `PDFLaTeX <http://www.latex-project.org/>`_, so an existing installation of PDFLaTeX
should exist in order to support this feature.

The PDF Generation creates a temporary directory on the filesystem per request. This directory is deleted and assured
to be deleted using ``try: ... finally: delete`` code. However, failures may occur, so this should be taken into
account.

For more information, refer to :mod:`edsudoku.server.pdf`.
