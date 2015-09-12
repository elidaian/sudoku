from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description
with open(path.join(here, 'DESCRIPTION.rst'), 'r') as f:
    long_description = f.read()

setup(
    name='edsudoku',
    version='2.0.dev1',
    description='Utility and website for generating solvable sudoku puzzles',
    long_description=long_description,
    url='https://github.com/elidaian/edsudoku',
    author='Eli Daian',
    author_email='elidaian@gmail.com',
    license='GPL',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ],
    keywords='sudoku server',
    packages=find_packages(),
    install_requires=['flask', 'sqlalchemy'],
    entry_points={
        'console_scripts': [
            'edsudoku-server=edsudoku.runserver:main',
            'edsudoku-init-db=edsudoku.server.init_db:main'
        ]
    }
)
