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

    # This is the file name that SQLite uses
    DATABASE = "sudoku.db"

    # Turned on when debug is enabled
    DEBUG = False

    # Secret key (generated using os.urandom). Regenerate for your configuration
    SECRET_KEY = "\x11\x96<\xdb\xd3$/\xc7\x82\xb3\xf7Zj\xe0n\\"

In newer versions, this file will be supplied with ``edsudoku`` package installation.
