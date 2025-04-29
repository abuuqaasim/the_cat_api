from logging import exception

import requests
import requests.packages
from typing import List, Dict
from .exception import TheCatAPIException
from json import JSONDecodeError
from the_cat_api.models import Result
import logging


class RestAdapter:
    def __init__(self, url: str, api_key='', ver='', ssl_verify: bool = True, logger: logging.Logger = None):
        self.url = "https://{}/{}/".format(url, ver)
        self.__api_key = api_key
        self.__ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        requests
        if not ssl_verify:
            # no inspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, end_point_params: Dict = None, data=None) -> Result:
        full_url = self.url + endpoint
        headers = {'x-api-key': self.__api_key}

        try:
            response = requests.request(http_method, endpoint)
        except requests.exceptions.RequestException("Request not granted!") as e:
            raise TheCatAPIException("Exiting") from e
        try:
            data = response.json()
            if 200 <= response.status_code <= 299:
                return Result(response.status_code, response.reason
                              , data)
        except (ValueError, JSONDecodeError) as e:
            raise TheCatAPIException('{response.status_code} :{response.reason}') from e

    def get(self, endpoint, end_point_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, end_point_params=end_point_params)

    def post(self, endpoint, end_point_params, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, end_point_params=end_point_params, data=data)

    def delete(self, endpoint, end_point_params, data) -> Result:
        return self._do(http_method="DELETE", endpoint=endpoint, end_point_params=end_point_params, data=data)

