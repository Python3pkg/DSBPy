from setuptools import setup

setup(
    name='DSBPy',
    version='0.3.0',
    author='Thor77',
    author_email='thor77@thor77.org',
    description='A Python-Interface for DSB',
    keywords='dsbpy dsb dasschwarzebrett school',
    url='https://github.com/Thor77/DSBPy',
    long_description='''
Python-Interface for DSB (Das Schwarze Brett)
Check the `Project <https://github.com/Thor77/DSBPy/>`_ for more information.
    ''',
    packages=['dsb'],
    install_requires=['requests', 'beautifulsoup4']
)
