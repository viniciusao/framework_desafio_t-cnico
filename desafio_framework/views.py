import builtins
import os

import request_logging.decorators
from basicauth.decorators import basic_auth_required
from django.http import HttpResponse

from .utils import JsonSlicer


@request_logging.decorators.no_logging(
    log_headers=False, log_body=False, log_response=True
)
@basic_auth_required
def retrieve_topmost(request):
    j = JsonSlicer(url=os.environ['TARGET'], properties_keys={'id', 'title'})
    response = j.get_json()
    if isinstance(response, builtins.dict):
        return HttpResponse(
            [response], content_type='application/json charset=utf-8',
            status=response['error']['status_code']
        )

    j.download(response.text)
    return HttpResponse(
        [j.get_properties(top=int(os.environ.get('TOPMOST_JSON_PROPERTIES')))],
        content_type='application/json charset=utf-8'
    )
