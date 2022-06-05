import os

import environ
import pytest

from .. import BASE_DIR
from ..utils import JsonSlicer

env = environ.Env()
environ.Env.read_env(BASE_DIR.joinpath('.env_dev'))


@pytest.mark.parametrize('status_code', [200, 404, 500])
def test_target_response(status_code):
    url_mocked = 'mock://www.target.com'
    j = JsonSlicer(url=url_mocked)
    j.mock_adapter.register_uri(
        'GET',
        url_mocked,
        status_code=status_code,
        text=''
    )
    r = j.get_json()
    error_reason = j.errors['not_json_response']['error']['reason']
    assert r or error_reason == r['error']['reason']


@pytest.mark.parametrize(
    'jsons_test, keys',
    [
        ('tests/todos_test.json', {'id', 'title'}),
        ('tests/todos_wrong_format.json', None),
        ('tests/todos_test.json', {'ide', 'tittle'}),
    ]
)
def test_json_parsing(jsons_test, keys):
    j = JsonSlicer(properties_keys=keys, json_path=BASE_DIR.joinpath(jsons_test))
    top_most = int(os.environ.get('TOPMOST_JSON_PROPERTIES'))
    parsed = j.get_properties(top=top_most)
    keys_error = j.errors['json_non_exist_keys']['error']['reason']
    json_parsing_error = j.errors['json_parsing']['error']['reason']
    assert len(parsed) == top_most or parsed['error']['reason'] in [keys_error, json_parsing_error]
