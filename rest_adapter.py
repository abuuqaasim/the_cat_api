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
        if not ssl_verify:
            # no inspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, end_point_params: Dict = None, data=None) -> Result:
        full_url = self.url + endpoint
        headers = {'x-api-key': self.__api_key}

        log_line_pre = f"methode={http_method}, url={full_url}, params={end_point_params}"
        log_line_post = ",".join((log_line_pre, "success={}, status_code={}, messaging={}"))

        try:
            self._logger.debug(msg=log_line_pre)   # Not needed except for debugging
            response = requests.request(http_method, endpoint)
        except requests.exceptions.RequestException("Request not granted!") as e:
            self._logger.error(msg=(str(e)))
            raise TheCatAPIException("Exiting") from e
        try:
            data = response.json()

        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, str(e)))
            raise TheCatAPIException("Bad JSON in response") from e
        is_success = 200 <= response.status_code <= 299
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code,response.reason, data)
        self._logger.error(msg=log_line)
        raise TheCatAPIException(f'{response.status_code}:{response.reason}')



    def get(self, endpoint, end_point_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, end_point_params=end_point_params)

    def post(self, endpoint, end_point_params, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, end_point_params=end_point_params, data=data)

    def delete(self, endpoint, end_point_params, data) -> Result:
        return self._do(http_method="DELETE", endpoint=endpoint, end_point_params=end_point_params, data=data)

