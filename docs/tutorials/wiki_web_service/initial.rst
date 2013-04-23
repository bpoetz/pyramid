.. _pyramid_webservice_wiki_tutorial:

Web Services Wiki Tutorial
=======================================


Let's start by making a simple change to the model to add an update timestamp.  This timestamp will show

1. edit models.py to add updated
2. update the initialize_db field
3. run the initialize_tutorial_db script to add the column to the DB.

Next we can modify our views.py

1. Remove anything to do with authentication and authorization including login/logout views
2. view_wiki now exists to serve a view that will use jquery ajax calls to interact with the wiki web service.
3. The wiki web service views are implemented as a class with get, post, and delete methods that map to the corresponding HTTP verbs.
4. Using a class takes advantage of the @view_defaults decorator to factor out the common name and renderer for each method.
5. In the get method, which used to be the view_page method, we've removed the check function and converted the functionality of it to return a list of WikiWords via re.findall. The old view_page function assumed that the wiki would be consumed in the context of an HTML page. Web services should not make assumptions about the context that the data will be used. Therefore, the hardcoded html markup was removed.
6. Note the use of request.json in the post method. WebOb will attempt to decode



Finally we want to alter our templates.

1. First we want to delete the unnecessary templates
2. We want to set the home page as a place to receive data from our web service.  We will use the venerable jQuery library - there are many different javascript libraries you may want to use to make interacting with the DOM easier, but that is beyond the scope of this tutorial.

3. add the jquery library to the page
4. add a page name area and an updated by area
5. add javascript to receive and send JSON


Testing

.. toctree::
   :maxdepth: 2

   initial
   web-service
   cornice
