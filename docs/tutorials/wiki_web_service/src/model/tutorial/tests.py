import unittest
import transaction

from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from tutorial.models import (
        DBSession,
        Page,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Page('FrontPage', 'This is the front page')
        DBSession.add(model)
    return DBSession


def _registerRoutes(config):
    config.add_route('page', '/{pagename}')


class PageModelTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def _getTargetClass(self):
        from tutorial.models import Page
        return Page

    def _makeOne(self, name='SomeName', data='some data'):
        return self._getTargetClass()(name, data)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.name, 'SomeName')
        self.assertEqual(instance.data, 'some data')


class ViewWikiTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, request):
        from tutorial.views import view_wiki
        return view_wiki(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        response = self._callFUT(request)
        self.assertEqual({}, response)


class PageGetTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from tutorial.views import PageView
        return PageView(request).get()

    def test_it(self):
        from datetime import datetime
        from tutorial.models import Page
        request = testing.DummyRequest()
        request.matchdict['pagename'] = 'IDoExist'
        page = Page('IDoExist', 'Hello CruelWorld IDoExist')
        self.session.add(page)
        _registerRoutes(self.config)
        resp = self._callFUT(request)
        self.assertEqual(resp['page'].name, 'IDoExist')
        self.assertEqual(resp['page'].data, 'Hello CruelWorld IDoExist')
        self.assertIsInstance(
            resp['page'].updated,
            datetime,
        )


class PagePostTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from tutorial.views import PageView
        return PageView(request).post()

    def test_page_post_update_page(self):
        from tutorial.models import Page
        _registerRoutes(self.config)
        page = Page('AnotherPage', 'hello yo!')
        self.session.add(page)
        request = testing.DummyRequest()
        request.matchdict = {'pagename': 'AnotherPage'}
        json = {'page': {'name': 'AnotherPage', 'data': 'Hello yo!'}}
        request.json = json
        self._callFUT(request)
        page = self.session.query(Page).filter_by(name='AnotherPage').one()
        self.assertEqual(page.data, 'Hello yo!')

    def test_page_post_create_page(self):
        from tutorial.models import Page
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        request.matchdict = {'pagename': 'AnotherPage'}
        json = {'page': {'name': 'AnotherPage', 'data': 'Hello yo!'}}
        request.json = json
        self._callFUT(request)
        page = self.session.query(Page).filter_by(name='AnotherPage').one()
        self.assertEqual(page.data, 'Hello yo!')


class PageDeleteTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from tutorial.views import PageView
        return PageView(request).delete()

    def test_page_post_delete_page(self):
        from tutorial.models import Page
        _registerRoutes(self.config)
        page = Page('AnotherPage', 'hello yo!')
        self.session.add(page)
        request = testing.DummyRequest(method='DELETE')
        request.matchdict = {'pagename': 'AnotherPage'}
        self._callFUT(request)
        page = self.session.query(Page).filter_by(name='AnotherPage').all()
        self.assertEqual([], page)


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from tutorial import main
        settings = {'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        _initTestingDB()

    def tearDown(self):
        del self.testapp
        from tutorial.models import DBSession
        DBSession.remove()

    def test_FrontPage(self):
        res = self.testapp.get('/FrontPage', status=200)
        self.assertTrue(b'page' in res.json)

    def test_unexisting_page(self):
        resp = self.testapp.get('/SomePage', status=200)
        self.assertTrue(b'error' in resp.json_body)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertEqual(res.location, None)
