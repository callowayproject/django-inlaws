=============
Django Inlaws
=============

Were you ever looking at a record in your Django admin and wonder what else that object was related to? Django Inlaws shows you the relations of the object automatically!

.. image:: http://github.com/callowayproject/django-inlaws/raw/master/doc_src/screenshot.png

Installation
============

Use pip or easy_install to install the package from PyPI::

	pip install django-inlaws

Usage
=====

Usage is very simple.

1. Add "inlaws" to your ``INSTALLED_APPS``.

2. Create an ``admin`` directory in your project's template directory.

3. Create a file called ``change_form.html`` in that ``admin`` directory.

4. The contents of the ``change_form.html`` file should be::

	{% extends "inlaws/change_form.html" %}