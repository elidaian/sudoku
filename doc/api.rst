``edsudoku`` API
****************

Boards
======

Boards represent the sudoku boards.

.. automodule:: edsudoku.board
    :members:

Board Generator
===============

The board generator is responsible for generating boards.

.. automodule:: edsudoku.generator
    :members:

Exceptions
==========

The exceptions that are raised from ``edsudoku`` are defined in :mod:`edsudoku.exceptions`.

.. automodule:: edsudoku.exceptions
    :members:

WSGI Server
===========

The complete implementation of the WSGI web server is available under the package :mod:`edsudoku.server`.

Static Content
--------------

There are three subdirectories of static content:

* :ref:`templates-dir`
* :ref:`static-dir`
* :ref:`fonts-dir`

.. _templates-dir:

The ``templates`` directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This directory contains the `Jinja2 <http://jinja.pocoo.org/>`_ templates for the website.

The available templates:

:``layout.html``: The page layout of most other HTML templates.

:``main_page.html``: Responsible for displaying the main page (see :func:`~edsudoku.server.login.main_page`).

:``login.html``: Responsible for displaying the login page (see :func:`~edsudoku.server.login.login`).

:``create_board.html``: Responsible for displaying the board generation form (see
    :func:`~edsudoku.server.my_boards.create_board`).

:``list_boards.html``: Responsible for listing the available boards (of this user, or of all users). It also allows
    selection of single or multiple boards, and displaying the problem or solution. See
    :func:`~edsudoku.server.my_boards.list_boards` and :func:`~edsudoku.server.other_users_boards.list_other_boards`.

:``html_board.html``: Provides a macro that generates a board template. Used by ``view_board.html`` and
    ``print_board.html``.

:``view_board.html``: Responsible for displaying a single board, or of multiple boards insite the website (see
    :func:`~edsudoku.server.view_boards.view_one_board` and :func:`~edsudoku.server.view_boards.view_many_boards`).

:``print_board.html``: Responsible for displaying a printable version of a single board, or of multiple boards (see
    :func:`~edsudoku.server.view_boards.view_one_board` and :func:`~edsudoku.server.view_boards.view_many_boards`).

:``list_users.html``: Responsible for listing the registered users (see
    :func:`~edsudoku.server.manage_users.manage_users`).

:``register.html``: Responsible for displaying the new users registration form (see
    :func:`~edsudoku.server.manage_users.register_user`).
:``delete_user.html``: Responsible for displaying the user deletion confirmation form (see
    :func:`~edsudoku.server.manage_users.delete_user`).

.. _static-dir:

The ``static`` directory
^^^^^^^^^^^^^^^^^^^^^^^^

This directory contains static content, not for rendering as templates, like the sources of `bootstrap
<http://getbootstrap.com/>`_ and `jQuery <https://jquery.com/>`_, and some other CSS files for customization of some
views.

The files in this directory are:

* `Bootstrap <http://getbootstrap.com/>`_ sources:

  * ``bootstrap.min.css``
  * ``bootstrap.min.js``
  * ``bootstrap-theme.min.css``

* `jQuery <https://jquery.com/>`_ 2.1.4 source:

  * ``jquery-2.1.4.min.js``

* Customizations:

  :``customization.css``: Self made customization theme of the bootstrap theme.

  :``board.css``: Some style guides for displaying the sudoku boards.

.. _fonts-dir:

The ``fonts`` directory
^^^^^^^^^^^^^^^^^^^^^^^

This directory contains `bootstrap <http://getbootstrap.com/>`_'s fonts.

The files in this directory are:

* ``glyphicons-halflings-regular.eot``
* ``glyphicons-halflings-regular.svg``
* ``glyphicons-halflings-regular.ttf``
* ``glyphicons-halflings-regular.woff``
* ``glyphicons-halflings-regular.woff2``

Backend Server Implementation
-----------------------------

The WSGI application is defined directly under the ``__init__.py`` file of :mod:`edsudoku.server`.
This file is responsible for defining, importing and loading the important functions of the web server.

Users
^^^^^

Some convenience objects for representing users and their permissions are defined in :mod:`edsudoku.server.users`.

.. automodule:: edsudoku.server.users
    :members:

DB Access
^^^^^^^^^

Some convenience DB functions for queries and updates are defined in the module :mod:`edsudoku.server.db`.

.. automodule:: edsudoku.server.db
    :members:

Converters
^^^^^^^^^^

Some `Werkzeug converters <http://werkzeug.pocoo.org/docs/0.10/routing/#custom-converters/>`_ were defined, in order to
ease the routing process.
These converters allow translation of URL parts to Python variables. For example, ``/true/`` would be converted to
``True``, and vice versa.

These converters are defined at the module :mod:`edsudoku.server.converters`.

.. automodule:: edsudoku.server.converters
    :members:

Logging In and Out
^^^^^^^^^^^^^^^^^^

The logic of logging in and out, and displaying the main page is implemented in :mod:`edsudoku.server.login`.

.. automodule:: edsudoku.server.login
    :members:

Generating and Viewing Boards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generic functions for viewing a single board or multiple boards are defined in :mod:`edsudoku.server.view_boards`.
This functionality includes viewing boards inside the website, or in a printable version.

.. automodule:: edsudoku.server.view_boards
    :members:

Viewing the boards of the current logged in user, and generating new board(s) for this user is implemented in
:mod:`edsudoku.server.my_boards`.

.. automodule:: edsudoku.server.my_boards
    :members:

Viewing the boards of all users is implemented in :mod:`edsudoku.server.other_users_boards`.

.. automodule:: edsudoku.server.other_users_boards
    :members:

Managing Users
^^^^^^^^^^^^^^

The logic of registering, editing and deleting users is implemented in :mod:`edsudoku.server.manage_users`.

.. automodule:: edsudoku.server.manage_users
    :members:

Miscellaneous
^^^^^^^^^^^^^

Some miscellaneous functionality of the web server is implemented in :mod:`edsudoku.server.misc`.
Some of its functionality includes:

* Opening and closing the DB connection (see :func:`~edsudoku.server.misc.open_db` and
  :func:`~edsudoku.server.misc.close_db`, respectively).
* Making sure that there is a logged in user, with the correct permissions for this page (see
  :func:`~edsudoku.server.misc.must_login`).
* Getting a font from :ref:`fonts-dir` (see :func:`~edsudoku.server.misc.get_font`).

.. automodule:: edsudoku.server.misc
    :members:

Internal Implementation
=======================

The internal implementation is located under the package :mod:`edsudoku.impl`.
A regular user should not use this package directly, it is used by the exported classes, and the internal
implementation may be changed at any time.

The internal implementation provides a more convenient representation of the objects in the sudoku board.
For more information about the role of each object, see :doc:`algorithms`.

A *board* consists of cells and groups.
For more information, see :class:`~edsudoku.impl.board.BoardImpl`.

A *cell* can have an assigned value or some possible values that can be assigned to it.
For more information, see :class:`~edsudoku.impl.cell.Cell`.

A *group* contains some cells of the board, such that two cells of the same group cannot have the same assigned value.
For more information, see :class:`~edsudoku.impl.group.CellGroup`.

.. automodule:: edsudoku.impl.cell
    :members:

.. automodule:: edsudoku.impl.group
    :members:

.. automodule:: edsudoku.impl.board
    :members:
