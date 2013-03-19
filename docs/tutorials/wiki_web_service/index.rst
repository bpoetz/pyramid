.. _pyramid_webservice_wiki_tutorial:

Web Services Wiki Tutorial
=======================================


This tutorial will explain how to use pyramid to build a web service that consumes and produces JSON.
We will build on the example given in the SQL alchemy tutorial.  We will assume you have already completed this tutorial.

For cut and paste purposes, the source code for all stages of this
tutorial can be browsed on GitHub at `docs/tutorials/wiki2/src
<https://github.com/Pylons/pyramid/tree/master/docs/tutorials/wiki_web_services/src>`_,
which corresponds to the same location if you have Pyramid sources.

.. toctree::
   :maxdepth: 2

   background
   design
   installation
   basiclayout
   definingmodels
   definingviews
   authorization
   tests
   distributing

Pyramid Web Services Tutorial

 Let's start by making a simple change to the model to add an update timestamp.

1. edit models.py to add updated
2. update the initialize_db field
3. run the initialize_tutorial_db script to add the column to the DB.

JSON does not natively support datetime serialization.

Next we can modify our views.py

1.  first



Finally we want to alter our templates.

1. First we want to delete the unnecessary templates
2. We want to set the home page as a place to receive data from our web service.  We will use the venerable jQuery library - there are many different javascript libraries you may want to use to make interacting with the DOM easier, but that is beyond the scope of this tutorial.

3. add the jquery library to the page
4. add a page name area and an updated by area
5. add javascript to receive and send JSON


Testing
