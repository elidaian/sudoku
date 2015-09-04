edsudoku
========

This is an utility and website for generating solvable sudoku puzzles.

Usage
-----

This utility can be used as a Python package, simply using `import edsudoku`.
For example, a regular sudoku board can be generated as follows:

```
import edsudoku
board = edsudoku.generate(3, 3)
```

In addition, edsudoku provides a WSGI web server application.
This application can be used using the following script:

```
from edsudoku.server import app as application.
```

Contact
-------

For any issue, please contact Eli Daian <elidaian@gmail.com>.
