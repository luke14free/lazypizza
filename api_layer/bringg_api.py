from datetime import datetime
import urllib
import json
import hmac
import hashlib
import requests
import calendar

BRINGG_ACCESS_TOKEN = 'yU5e5hHGbUXnYccT7ert'
BRINGG_SECRET_KEY = 'QSGpaTQbwUvrS_Nj4zFd'
COMPANY_ID = 2782


def api_call(url, params, method):
    params = json.loads(json.dumps(params)) #converts python objects to javascript like objects
    params['timestamp'] = calendar.timegm(datetime.utcnow().utctimetuple())
    params['access_token'] = BRINGG_ACCESS_TOKEN
    params['signature'] = hmac.new(BRINGG_SECRET_KEY, msg=urllib.urlencode(params), digestmod=hashlib.sha1).hexdigest()

    if method.lower() == "post":
        f_method = "post"
        r = requests.post(url, params=params)
    elif method.lower() == "get":
        f_method = "get"
        r = requests.get(url, params=params)
    elif method.lower() == "patch":
        f_method = "patch"
        r = requests.patch(url, params=params)
    elif method.lower() == "delete":
        f_method = "delete"
        r = requests.delete(url, params=params)
    return {'status': r.status_code, 'response': r.text, 'request_url': r.url, 'method': f_method}


def create_user(company_id, name, email, password, phone, admin=False):
    params = {
        "company_id": company_id,
        "name": name,
        "email": email,
        "password": password,
        "phone": phone,
        "admin": admin
    }

    return api_call(
        "http://developer-api.bringg.com/partner_api/users",
        params,
        "POST"
    )


def create_company(company_name, phone):
    return api_call(
        "http://developer-api.bringg.com/partner_api/companies",
        {
            'name': company_name,
            'phone': phone
        },
        "POST"
    )


def create_task(customer_id, company_id, address, total_price, asap=True, note=""):
    params = {
        "customer_id": customer_id,
        "company_id": company_id,
        "note": note,
        "address": address,
        "total_price": total_price,
        "asap": asap
    }

    return api_call(
        "http://developer-api.bringg.com/partner_api/tasks",
        params,
        "POST"
    )


def create_customer(name, company_id, address, phone):
    params = {
        "name": name,
        "company_id": company_id,
        "address": address,
        "phone": phone
    }

    return api_call(
        "http://developer-api.bringg.com/partner_api/customers",
        params,
        "POST"
    )