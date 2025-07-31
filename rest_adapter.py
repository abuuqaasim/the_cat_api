from logging import exception

import requests
import requests.packages
from typing import List, Dict
from .exception import TheCatAPIException
from json import JSONDecodeError
from the_cat_api.models import Result
import logging

'''
The phrase “based on the class name” is a bit of shorthand: the __name__ variable typically contains the module name. If this code is part of a module named rest_adapter, then getLogger(__name__) returns a logger named 'rest_adapter'
'''

class RestAdapter:
    def __init__(self, url: str, api_key='', ver='', ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param url: Typically, api.thecatapi.com
        :param api_key: (optional) string used for authentication when POSTing and DELETEing
        :param ver:  always v1 here
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) if your app has a logger, it should be passed here
        """
        self.url = "https://{}/{}/".format(url, ver)
        self.__api_key = api_key
        self.__ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            # no inspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()
            
             

    def _do(self, http_method: str, endpoint: str, end_point_params: Dict = None, data=None) -> Result:
        """

        :param http_method:
        :param endpoint:
        :param end_point_params:
        :param data:
        :return:
        """
        full_url = self.url + endpoint
        headers = {'x-api-key': self.__api_key}

        log_line_pre = f"method={http_method}, url={full_url}, params={end_point_params}"
        log_line_post = ",".join((log_line_pre, "success={}, status_code={}, messaging={}"))

        #Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)   # Not needed except for debugging
            response = requests.request(http_method, endpoint)
        except requests.exceptions.RequestException("Request not granted!") as e:
            self._logger.error(msg=(str(e)))
            raise TheCatAPIException("Exiting") from e

        #Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data = response.json()

        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, str(e)))
            raise TheCatAPIException("Bad JSON in response") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 200 <= response.status_code <= 299
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code,response.reason, data)
        self._logger.error(msg=log_line)
        raise TheCatAPIException(f'{response.status_code}:{response.reason}')



    def get(self, endpoint, end_point_params: Dict = None) -> Result:
        """

        :param endpoint:
        :param end_point_params:
        :return:
        """
        return self._do(http_method='GET', endpoint=endpoint, end_point_params=end_point_params)

    def post(self, endpoint, end_point_params, data: Dict = None) -> Result:
        """

        :param endpoint:
        :param end_point_params:
        :param data:
        :return:
        """
        return self._do(http_method='POST', endpoint=endpoint, end_point_params=end_point_params, data=data)

    def delete(self, endpoint, end_point_params, data) -> Result:
        """

        :param endpoint:
        :param end_point_params:
        :param data:
        :return:
        """
        return self._do(http_method="DELETE", endpoint=endpoint, end_point_params=end_point_params, data=data)

