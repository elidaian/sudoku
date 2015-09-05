Implementation Algorithms
*************************

Representation in the Implementation
====================================

The implementation consists of three building blocks:

* :ref:`cells`
* :ref:`groups`
* :ref:`board`

.. _cells:

Cells
-----

A *cell* can have an assigned value or some possible values that can be assigned to it.
Each cell can be a member of several :ref:`groups`.

Each cell is initialized with an *alphabet* of possible *symbols*.
A symbol is *possible* to be assigned in a cell if this symbol is not assigned in any other cell that has at least one
common group with the cell.

A value or symbol can be assigned to a cell only if this symbol is in the alphabet, and this symbol is possible to be
assigned.

Each time a symbol is assigned to a cell, this cell updates all other cells in its groups that this symbol is not
possible any more.

Cells are implemented in the class :class:`~edsudoku.impl.cell.Cell`.

.. _groups:

Cell Groups
-----------

A *cell group* consists of several cells.
For example, a row of cells is a cells group.

A symbol is said to be *assigned in a group* if it is assigned in a cell that is a member of the group.

Each symbol can be assigned at most once in a group.

Cell groups are implemented in the class :class:`~edsudoku.impl.group.CellGroup`.

.. _board:

Board
-----

A *board* consists of cells, cell groups and alphabet.
It also has a defined dimensions, which are derived from the block dimensions.

The groups in each board are:

* The **row**\ s.
* The **column**\ s.
* | The **block**\ s.
  | These are the smaller rectangles inside the board, that cannot have a symbol assigned twice or more in them.

Boards are implemented in the class :class:`~edsudoku.impl.board.BoardImpl`.

Solving a Board
===============

This algorithm aims to solve the board as much as possible. The resolution process does not guess at any step, and
solves only cells that have a certain value.

* Run in a loop, until no change is done or the board is fully solved:

  #. | Fill cells that have only one possible symbol with the only possible symbol.
     | See :meth:`~edsudoku.impl.board.BoardImpl._fill_one_possible` for implementation.
  #. | Split groups when possible.
     | A group of size :math:`n` can be split if there is a subgroup of size :math:`0 < k < n` cells in this group,
       such that these cells have the same :math:`k` possible symbols. In this case, this group can be considered as
       two different groups. The subgroup with a possible alphabet of the :math:`k` symbols, and the complementary
       subgroup.
     | See :meth:`~edsudoku.impl.board.BoardImpl._split_groups` for implementation.
  #. | Remove cells with assigned values from the groups.
     | This step improved the performance of the algorithm when implemented, since cells with the assigned values are
       no more needed in the groups, but they are being notified for every assigned symbol in their groups.
     | See :meth:`~edsudoku.impl.board.BoardImpl._remove_assigned_from_groups` for implementation.
  #. | Remove possible symbols from cells.
     | If a symbol is possible in only :math:`n` cells of a group, and all these $n$ cells are also a part of another
       group, this symbol should not be possible in any other cell of the other group.
     | See :meth:`~edsudoku.impl.board.BoardImpl._remove_from_other_groups` for implementation.
  #. | *Optional:* Remove empty groups.
     | This step improved the performance of the algorithm implementation, since the algorithm has no need in empty
       groups.
     | See :meth:`~edsudoku.impl.board.BoardImpl._remove_empty_groups` for implementation.

The logic of this implementation is available at :meth:`~edsudoku.impl.board.BoardImpl.solve_possible`.

Generating a Board
==================

TODO.
