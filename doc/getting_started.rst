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

    print 'Problem board:'
    for row in xrange(board.rows):
        for col in xrange(board.cols):
            print board.problem[row, col],
        print

    print 'Solved board:'
    for row in xrange(board.rows):
        for col in xrange(board.cols):
            print board.solution[row, col],
        print

Note that the arguments ``3, 3`` that were passed to :func:`~edsudoku.generator.generate` indicates the block
dimensions in the board. The board dimensions are later derived from the block dimensions.

Also note that the returned board contains both the problem and the solution for this problem, and it is easy to get
the cells of each block.
