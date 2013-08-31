"""
pdf_renderer.py

 Created on: Aug 31 2013
     Author: eli
"""

from flask import Response
import os
import shutil
import subprocess
import tempfile

### FUNCTIONS ###

def create_env(app):
    """
    Create a TeX environment.
    """
    texenv = app.create_jinja_environment()
    texenv.block_start_string = '((*'
    texenv.block_end_string = '*))'
    texenv.variable_start_string = '((('
    texenv.variable_end_string = ')))'
    texenv.comment_start_string = '((='
    texenv.comment_end_string = '=))'
    return texenv

def make_pdf(tex):
    """
    Make a PDF file from the given source.
    """
    try:
        tmp_dir = tempfile.mkdtemp()
        tex_file = os.path.join(tmp_dir, "doc.tex")
        pdf_file = os.path.join(tmp_dir, "doc.pdf")
        
        with open(tex_file, "w") as f:
            f.write(tex)
        
        p = subprocess.Popen(["pdflatex", "-interaction", "nonstopmode", tex_file],
                             cwd=tmp_dir, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        
        with open(pdf_file, "rb") as f:
            return f.read()
    finally:
        shutil.rmtree(tmp_dir)

def render_pdf_template(template, texenv, **kwargs):
    """
    Render a pdf template.
    """
    tex = texenv.get_template(template).render(**kwargs)
#     return tex
    pdf = make_pdf(tex)
    return Response(pdf, mimetype="application/pdf")
