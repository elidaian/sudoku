Introduction
************

``edsudoku`` is an utility and website for generating solvable sudoku puzzles.
It is named after its developer, Eli Daian.

Basic Motivation
================

This software package is originated in a C package called `Sudoku Sensei <http://sudoku-sensei.sourceforge.net/>`_.
The need is print lot of new sudoku boards for a friend of the developer. Sudoku Sensei (in an early version) had a
command line interface for generating boards, including boards of unconventional size (like :math:`12 \times 12`, where
each cells block is :math:`3 \times 4` cells).

So this package was downloaded by the developer, and changed so it created HTML pages from the command line interface.
Since the friend wanted the puzzles in batches, it was more convenient to print them together, and not each HTML file
by its own. Hence, a Python script that combined the boards into a single HTML page was created.

At the next step, hints were requested from that friend. Therefore, all generated boards were stored, each board with
its unique ID. The boards were stored simply on the filesystem. Querying a board for extracting a hint became a complex
operation, since one needed to find a file in a directory that contains lot of files, which caused the operating system
to list a large directory.

Therefore, a complete software package was developed. This package allows convenient generation of boards and a
convenient method to query for a board (even if there are lot of boards in the system). The interface is a website, so
every user can use this framework.

Current Features
================

This software package does not depend on the original Sudoku Sensei. It has its own pure Python implementation of
sudoku boards generation (tough it is slower than the C implementation).

Current technologies being used:

* The web server is implemented on top of the `Flask <http://flask.pocoo.org/>`_ framework, that implements the
  `Web Server Gateway Interface (WSGI) <https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_.
* The boards are stored in an `SQLite <https://www.sqlite.org/>`_ database, powered on Python's |sqlite3 module|_.
* The website uses `bootstrap <http://getbootstrap.com/>`_ as a good CSS infrastructure.
* The website uses `jQuery <https://jquery.com/>`_ as a basic JavaScript library.

.. |sqlite3 module| replace:: ``sqlite3`` module
.. _sqlite3 module: https://docs.python.org/2/library/sqlite3.html

Future plans:

* Use |sqlalchemy|_ for DB usage, in order to support any DB engine.
* Add an accelerator C module, and thus provide cross compatibility with any Python interpreter, and allowing faster
  computations.
* Use `Jade <http://jade-lang.com/>`_ and `Stylus <https://learnboost.github.io/stylus/>`_ for easier development of
  the templates.

.. |sqlalchemy| replace:: ``sqlalchemy``
.. _sqlalchemy: http://www.sqlalchemy.org/
