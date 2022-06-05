import builtins
import os
from typing import Dict, List, Optional, Set, Union

import ijson
import requests
import requests_mock
from ijson.common import IncompleteJSONError

from . import BASE_DIR


class JsonSlicer:

    errors = {
        'not_json_response': {'error': {
            'reason': 'not able to retrieve target\'s contents.',
        }},
        'json_parsing': {'error': {
            'reason': 'JSON Parsing error.'
        }},
        'json_non_exist_keys': {'error': {
            'reason': 'JSON Properties keys don\'t exist.'
        }}
    }

    def __init__(
            self,
            *,
            url: builtins.str = None,
            properties_keys: Set[builtins.str] = None,
            json_path: builtins.str = None
    ) -> None:

        self.mock_adapter = requests_mock.Adapter()
        self.client = self._client_setup()
        self.json_path = BASE_DIR.joinpath(os.environ.get('JSON_NAME')) if not json_path else json_path
        self.json_format_keys = properties_keys
        self.url = url

    def _client_setup(self) -> requests.Session:
        session = requests.Session()
        session.mount('mock://', self.mock_adapter)
        return session

    def get_json(self):
        return self._request()

    def get_properties(self, *, top: builtins.int):
        try:
            return self._properties_format(top)
        except IncompleteJSONError as e:
            error = self.errors['json_parsing']
            error['error'].update({'exception': e.args[0]})
            return error

    def _request(self) -> Union[requests.Response, Dict]:
        response = self.client.get(self.url)
        status_code = response.status_code
        if status_code == 200:
            return response
        else:
            not_json = self.errors['not_json_response']
            not_json['error'].update({'status_code': status_code})
            return not_json

    def _properties_format(self, top: builtins.int) -> Union[Dict, List]:
        with open(self.json_path, 'r+') as f:
            json_ = ijson.items(f, 'item')
            how_much = []
            for counter, property_ in enumerate(json_, start=1):
                if not counter <= top:
                    break
                properties = self._pop_keys(property_)
                if 'error' in properties:
                    return properties
                how_much.append(properties)
            return how_much

    def download(self, json_) -> None:
        with open(self.json_path, 'w+') as f:
            f.truncate()
            f.writelines(json_)

    def _pop_keys(self, dict_) -> Dict:
        keys = {k: v for k, v in dict_.items() if k in self.json_format_keys}
        non_exist_keys = self.errors['json_non_exist_keys']
        non_exist_keys['error'].update(
            {'keys': self.json_format_keys, 'status_code': 500}
        )
        return keys if keys else non_exist_keys
