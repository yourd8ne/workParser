import requests

webhook_url1 = 'https://cloud.roistat.com/integration/webhook?key=a58c86c38a259de63562d533d7c7edf4'

webhook_url2 = 'https://c6ce863bb1eb.vps.myjino.ru/contacts?apiKey=Wy7RXAzSRZpD4a3q'

data1 = {
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

data2 = {
    "source":"название сайта (например joblab.ru)",
    "name": "Имя контакта",
    "email":"email контакта",
    "phone":"телефон контакта",
    "data":"ссылка на вакансию;Имя контакта;email контакта;телефон контакта;Адрес вакансии или город"
}

response1 = requests.post(webhook_url1, json=data1)
response2 = requests.post(webhook_url2, json=data2)

print("Response1 from webhook:", response1.text)
print("Response2 from webhook:", response2.text)
