__version__ = '1.0.0'
import sys
from hashlib import sha1, md5
from collections import OrderedDict
import hmac
import requests
from requests.models import RequestEncodingMixin as urlencode
import base64

class ZadarmaAPI(object):

    def __init__(self, key, secret, is_sandbox=False):
        """
        Constructor
        :param key: key from personal
        :param secret: secret from personal
        :param is_sandbox: (True|False)
        """
        self.key = key
        self.secret = secret
        self.is_sandbox = is_sandbox
        self.__url_api = 'https://api.zadarma.com'
        if is_sandbox:
            self.__url_api = 'https://api-sandbox.zadarma.com'

    def call(self, method, params={}, request_type='GET', format='json', is_auth=True):
        """
        Function for send API request
        :param method: API method, including version number
        :param params: Query params
        :param request_type: (get|post|put|delete)
        :param format: (json|xml)
        :param is_auth: (True|False)
        :return: response
        """
        request_type = request_type.upper()
        allowed_type = ['GET', 'POST', 'PUT', 'DELETE']
        if request_type not in allowed_type:
            request_type = 'GET'
        params['format'] = format
        auth_str = None
        if is_auth:
            auth_str = self.__get_auth_string_for_header(method, params)

        result = False
        if request_type == 'GET':
            sorted_payload = OrderedDict(sorted(params.items()))
            request_url = self.__url_api + method
            result = requests.get(request_url, params=sorted_payload, headers={'Authorization': auth_str})
        elif request_type == 'POST':
            result = requests.post(self.__url_api + method, headers={'Authorization': auth_str}, data=params)
        elif request_type == 'PUT':
            result = requests.put(self.__url_api + method, headers={'Authorization': auth_str}, data=params)
        return result.text

    def __get_auth_string_for_header(self, method, params):
        """
        :param method: API method, including version number
        :param params: Query params dict
        :return: auth header
        """
        sorted_payload = urlencode._encode_params(OrderedDict(sorted(params.items())))
        md5hash = md5(sorted_payload.encode('utf8')).hexdigest()
        data = method + sorted_payload + md5hash
        hmac_h = hmac.new(self.secret.encode('utf8'), data.encode('utf8'), sha1)
        if sys.version_info.major > 2:
            bts = bytes(hmac_h.hexdigest(), 'utf8')
        else:
            bts = bytes(hmac_h.hexdigest()).encode('utf8')
        auth = self.key + ':' + base64.b64encode(bts).decode()
        return auth
