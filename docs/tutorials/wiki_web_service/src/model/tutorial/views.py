import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from .models import (
    DBSession,
    Page,
    )

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='view_wiki')
def view_wiki(request):
    return HTTPFound(location = request.route_url('view_page',
                                                  pagename='FrontPage'))

@view_config(route_name='page_get', request_method='GET',
             renderer='json')
def page_get(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        return dict(error='No such page')

    return dict(page=page, wikiwords=wikiwords.findall(page.data))

@view_config(route_name='page_post', request_method='POST',
             renderer='json')
def page_post(request):
    pagename = request.matchdict['pagename']
    data = request.POST['page']

    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page:
        DBSession.update(**data)
        page = DBSession.query(Page).filter_by(name=pagename).first()
    else:
        page = Page(**data)
        DBSession.add(page)
    return dict(page=page)
