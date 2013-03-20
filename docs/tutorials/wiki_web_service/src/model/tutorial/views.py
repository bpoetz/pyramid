import re

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    view_defaults,
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


@view_defaults(route_name='page', renderer='json')
class PageView(object):

    def __init__(self,request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        pagename = self.request.matchdict['pagename']
        page = DBSession.query(Page).filter_by(name=pagename).first()
        if page is None:
            return dict(error='No such page', name=pagename)

        return dict(page=page, wikiwords=wikiwords.findall(page.data))

    @view_config(request_method='POST')
    def post(self):
        name = self.request.matchdict['pagename']
        page_data = self.request.json['page']

        page = DBSession.query(Page).filter_by(name=name).first()
        if page:
            page.data = page_data['data']
        else:
            page = Page(name=name, data=page_data['data'])
            DBSession.add(page)

        return dict(page=page, wikiwords=wikiwords.findall(page.data))

    @view_config(request_method='DELETE')
    def delete(self):
        pagename = self.request.matchdict['pagename']

        page = DBSession.query(Page).filter_by(name=pagename).first()
        if page:
            DBSession.delete(page)
        else:
            return dict(error='No such page')

        return dict()
