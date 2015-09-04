Getting Started
***************

Before getting started, make sure you have an :doc:`installed </installation>` version of ``edsudoku``.

Python Interface
================

In order to use ``edsudoku`` from Python, simply run:

.. code-block:: python

    import edsudoku

Board Generation
----------------

This is an example for generating a regular sudoku board, and printing it:

.. code-block:: python

    board = edsudoku.generate(3, 3)
    for row in xrange(board.rows):
        for col in xrange(board.cols):
            print board[row, col],
        print

Note that the arguments ``3, 3`` that were passed to :meth:`~edsudoku.generator.generate` indicates the block
dimensions in the board. The board dimensions are later derived from the block dimensions.
