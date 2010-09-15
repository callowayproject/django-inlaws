=============
Django InLaws
=============

Were you ever looking at a record in your Django admin and wonder what else that object was related to? Django-InLaws shows you the relations of the object automatically!

.. image:: http://github.com/washingtontimes/django-inlaws/raw/master/doc_src/screenshot.png

**This is a proof of concept/request for comments release**

Installation
============

Use pip or easy_install to install the package from PyPI::

	pip install django-inlaws

or::

	easy_install django-inlaws

Or checkout the source from `github <http://github.com/washingtontimes/django-inlaws>`_ and run::

	python setup.py install

Usage
=====

Usage is very simple.

1. Add "inlaws" to your ``INSTALLED_APPS``\ .

2. Create an "admin" directory in your project's template directory.

3. Create a file called ``change_form.html``\ .

4. The contents of the file should be::

	{% extends "inlaws/change_form.html" %}