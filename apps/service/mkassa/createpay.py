import requests

MKASSA_BASE = "https://api.mkassa.kg"
LOGIN_DATA = {
    "login": "251171",
    "password": "YzUYANPws",
    "device_uuid": "PI"
}


def mkassa_login():
    url = f"{MKASSA_BASE}/api/users/login/"
    response = requests.post(url, data=LOGIN_DATA)
    return response


def mkassa_create_payment(token, payment_amount, products):
    url = f"{MKASSA_BASE}/api/v1/qr_payments/init_payment/"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "payment_amount": payment_amount,
        "products": products
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def mkassa_check_payment(token, payment_id):
    url = f"{MKASSA_BASE}/api/qr_payments/{payment_id}/check"
    headers = {
        "Authorization": token
    }
    response = requests.options(url, headers=headers)  
    return response
