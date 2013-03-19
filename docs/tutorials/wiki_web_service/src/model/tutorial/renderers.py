import datetime
from pyramid.renderers import JSON

json_renderer = JSON()


def datetime_adapter(obj, request):
    return obj.isoformat()

json_renderer.add_adapter(datetime.datetime, datetime_adapter)
