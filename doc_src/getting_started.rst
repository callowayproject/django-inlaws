===============
Getting Started
===============

Django Inlaws is a pluggable app that requires very little to get it working in your project.

1. Add "inlaws" to your ``INSTALLED_APPS`` setting in your project's ``settings.py`` file.

2. Create an "admin" directory in your project's template directory. ::

	MyProject
	+- templates
	   +- admin

3. Create a file called ``change_form.html``\ . ::

	MyProject
	+- templates
	   +- admin
	      `- change_form.html

4. The contents of the file should be::

	{% extends "inlaws/change_form.html" %}

What items are shown
====================

Several criteria must be met:

1. The model has a ``ForeignKey``\ , ``ManyToManyField``\ , or ``OneToOneField`` field in its model. For example ``django.contrib.comments.models.Comment`` has a ``ForeignKey`` related to ``User``\ . Therefore ``Comment`` entries will be displayed on the appropriate ``User``\ 's admin change form.

2. The model has a registered ``ModelAdmin`` class. For example, ``django.contrib.admin.models.LogEntry`` has a ``ForeignKey`` relating to ``User``\ , but does not have a ``ModelAdmin`` registered. Therefore you will not see any ``LogEntry`` items on any ``User`` change form.

3. The model is not in the :ref:`ADMIN_RELATED_EXCLUDES <admin_related_excludes>` setting. This setting allows you to specifically exclude models from appearing, even in the first two criteria are met. ``ADMIN_RELATED_EXCLUDES`` is simply a list or tuple of strings in ``'appname.model'`` format.