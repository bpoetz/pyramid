import re

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


@view_config(route_name='home', renderer='templates/view.pt')
def view_wiki(request):
    return dict()


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
    page_post_data = request.POST['page']

    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page:
        page.data = page_post_data['data']
    else:
        page = Page(**page_post_data)
        DBSession.add(page)

    return dict(page=page)


@view_config(route_name='page_delete', request_method='DELETE',
             renderer='json')
def page_delete(request):
    pagename = request.matchdict['pagename']

    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page:
        DBSession.delete(page)
    else:
        return dict(error='No such page')

    return dict()
