import os
import sys

latex_engine = "xelatex"

root_abs_path = os.path.abspath('../..')
sys.path.insert(0, root_abs_path)


PYTHON_EXECUTABLE = os.path.join(root_abs_path, 'env', 'bin', 'python')


def build_material() -> None:
    for nb_filepath in os.listdir('../material'):
        if nb_filepath.rsplit('.', 1)[-1] == 'ipynb':
            nb_filepath = os.path.join('../material', nb_filepath)
            python_converted_script = nb_filepath.replace('.ipynb', '.py')
            if os.name == 'nt':
                os.system(
                    f'{PYTHON_EXECUTABLE} -m jupyter nbconvert {nb_filepath} --to python && {PYTHON_EXECUTABLE} {python_converted_script} && del {python_converted_script}'
                )
            else:
                os.system(
                    f'{PYTHON_EXECUTABLE} -m jupyter nbconvert {nb_filepath} --to python && {PYTHON_EXECUTABLE} {python_converted_script} && rm {python_converted_script}'
                )


if os.environ.get('BUILDMATERIAL', 'FALSE').lower().strip() in [
    '0',
    'false',
    'no',
    'ignore',
    'skip',
]:
    print('Skipping material build as requested')
else:
    print('Material building started...')
    try:
        build_material()
        print('Build successed!')
    except Exception as e:
        print('Build failed.', e)

from italy_geopop import __version__

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'italy-geopop'
copyright = '2023, Zeno Dalla Valle'
author = 'Zeno Dalla Valle'
release = __version__.rsplit('.', 1)[0]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
html_js_files = ['js/custom.js']
html_css_files = ['css/custom.css']
