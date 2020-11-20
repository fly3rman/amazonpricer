from setuptools import setup

setup(
    name = 'amazon price parser',
    version = '0.1',
    install_requires = [
        'pandas',
        'bs4', 
        'tabulate', 
        'Click'],
    py_modules = ['amazonpricer'],
    entry_points = """
    [console_scripts]
    huhu=amazonpricer:huhu []
    ap=amazonpricer:main []
    """
)