import httpx


def send_notification(bundle_id, auth_token, device_id):
    url = "https://api.development.push.apple.com/3/device/" + device_id
    headers = {
        "apns-expiration": "0",
        "apns-priority": "10",
        "apns-topic": bundle_id,
        "authorization": "bearer " + auth_token,
    }
    payload = {
        "aps": {
            "alert": "Test for no name dig it all webhook!",
            "sound": "default",
            "badge": 1,
        },
    }
    with httpx.Client(http2=True) as client:
        response = client.post(url, headers=headers, json=payload)
    return response
