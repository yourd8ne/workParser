import requests

webhook_url = 'https://cloud.roistat.com/integration/webhook?key=a58c86c38a259de63562d533d7c7edf4'


data = {
    'key1': 'value1',
    'key2': 'value2'
}

response = requests.post(webhook_url, json=data)

print("Response from webhook:", response.text)
