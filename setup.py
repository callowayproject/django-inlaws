import os
from setuptools import setup, find_packages

def read_file(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(
    name = "django-inlaws",
    version = __import__('inlaws').get_version().replace(' ', '-'),
    url = 'http://github.com/washingtontimes/django-inlaws',
    author = 'Corey Oordt, Jose Soares, Justin Quick',
    author_email = 'webdev@washingtontimes.com',
    description = 'Shows related objects in the Django admin.',
    long_description = read_file('README.rst'),
    packages = find_packages(),
    include_package_data = True,
    install_requires=read_file('requirements.txt'),
    classifiers = [
    ],
)
