from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from .renderers import json_renderer


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory='tutorial.models.RootFactory')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('page_get', '/{pagename}')
    config.add_route('page_post', '/{pagename}')
    #config.add_route('page_delete', '/{pagename}')
    config.add_renderer('json', json_renderer)
    config.scan()
    return config.make_wsgi_app()
