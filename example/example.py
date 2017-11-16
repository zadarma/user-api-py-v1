#!/usr/bin/python3

from zadarma import api

if __name__ == '__main__':
    z_api = api.ZadarmaAPI(key='YOU_KEY', secret='YOUR_SECRET')
    # get tariff information
    z_api.call('/v1/tariff/')
    # set callerid for your sip number
    z_api.call('/v1/sip/callerid/', {'id': '1234567', 'number': '71234567890'}, 'PUT')
    # get information about coast
    z_api.call('/v1/info/price/', {'number': '71234567891', 'caller_id': '71234567890'})
