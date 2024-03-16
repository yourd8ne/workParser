import requests

webhook_url = 'https://cloud.roistat.com/integration/webhook?key=a58c86c38a259de63562d533d7c7edf4'


data = {
    "title":"Название вакансии",
    "name":"Имя контакта",
    "email":"email контакта",
    "phone":"телефон контакта",
    "comment":"ссылка на вакансию",
    "roistat_visit":"название сайта (например joblab.ru)",
    "fields":{"site":"название сайта (например joblab.ru)",
    "source":"название сайта (например joblab.ru)",
    "promocode":'null'}
}

response = requests.post(webhook_url, json=data)

print("Response from webhook:", response.text)
