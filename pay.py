import requests
import json

CERT_FILE = 'huzur_client.crt'      
KEY_FILE = 'huzur_pKey.pem'         

URL = 'https://3ds-test.demirbank.kg:8443/payments/v1/create'

payload = {
    "merchantId": "POSISOMRCH01",
    "terminalId": "POSISO01",
    "txnCode": 1,
    "amttxn": 3500,
    "curtxn": "840",
    "detail": "Purchase transaction",
    "channelCode": "CRD3DS20",
    "language": "EN",
    "paymentDate": "2025-07-12T00:00:00Z",
    "clientIp": "158.181.206.180",
    "returnUrl": "https://localhost:6343/signin"
}

try:
    response = requests.post(
        URL,
        json=payload,
        cert=(CERT_FILE, KEY_FILE), 
        headers={'Content-Type': 'application/json'},
        verify=False  
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

except requests.exceptions.RequestException as e:
    print("Ошибка при подключении:", e)
