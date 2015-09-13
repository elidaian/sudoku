from subprocess import Popen, PIPE
from tempfile import mkdtemp
from shutil import rmtree
from os.path import join, isfile

from flask.helpers import send_file
from werkzeug.exceptions import InternalServerError

from edsudoku.server import app

__author__ = 'Eli Daian <elidaian@gmail.com>'


def _create_env():
    """
    Create a new Jinja2 environment for rendering TeX with the custom escapings.

    :return: The created environment.
    :rtype: :class:`flask.templating.Environment`
    """
    latex_env = app.create_jinja_environment()
    latex_env.block_start_string = '((*'
    latex_env.block_end_string = '*))'
    latex_env.variable_start_string = '((('
    latex_env.variable_end_string = ')))'
    latex_env.comment_start_string = '((='
    latex_env.comment_end_string = '=))'
    return latex_env


def _tex_to_pdf(tex, filename):
    """
    Convert LaTeX data to PDF using ``pdflatex``. The result would be Flask's :func:`~flask.helpers.send_file`.

    :param tex: The LaTeX data.
    :type tex: str
    :param filename: Filename for the downloaded file (in the user side).
    :type filename: str
    :return: A :func:`~flask.helpers.send_file`.
    :rtype: flask.Response
    """

    tmp_dir = None
    try:
        tmp_dir = mkdtemp()
        tex_file = join(tmp_dir, 'doc.tex')
        pdf_file = join(tmp_dir, 'doc.pdf')

        with open(tex_file, 'w') as tf:
            tf.write(tex)

        p = Popen(['pdflatex', '-interaction', 'nonstopmode', tex_file],
                  cwd=tmp_dir, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.communicate()

        if p.returncode != 0 or not isfile(pdf_file):
            raise InternalServerError()

        return send_file(pdf_file, as_attachment=True, attachment_filename=filename)
    finally:
        if tmp_dir:
            rmtree(tmp_dir, ignore_errors=True)


def render_pdf_template(template, filename=None, **kwargs):
    """
    Render a PDF file from a template, like the :func:`~flask.templating.render_template` function.

    This function is responsible for:

    #. Generating a LaTeX file.
    #. Invoking ``pdflatex`` for transforming this LaTeX file to a PDF file.

    :param template: The template file name.
    :type template: str
    :param filename: The file name, as should be sent to the user to download as, or ``None`` for no file name.
    :type filename: str
    :param kwargs: Keyword arguments to be passed to Jinja2.
    :type kwargs: dict
    :return: A response object.
    :rtype: flask.Response
    """
    tex = _create_env().get_template(template).render(**kwargs)
    return _tex_to_pdf(tex, filename)
