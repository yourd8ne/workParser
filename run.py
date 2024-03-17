import json
import requests
from urllib.parse import urlparse
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
}

url = 'https://api.zp.ru/v1/vacancies'

def save_processed_vacancies(processed_vacancies):
    with open('processed_vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(list(processed_vacancies), file, ensure_ascii=False, indent=4)

def mark_vacancy_as_processed(vacancy_id, processed_vacancies):
    processed_vacancies.add(vacancy_id)
    save_processed_vacancies(processed_vacancies)

def is_vacancy_processed(vacancy_id, processed_vacancies):
    return vacancy_id in processed_vacancies

def should_process_vacancy(vacancy_id, processed_vacancies):
    if is_vacancy_processed(vacancy_id, processed_vacancies):
        return False
    else:
        return True

def req():
    limit = 100
    all_data = {'metadata': {}, 'vacancies': []}
    
    processed_vacancies = set()
    try:
        with open('processed_vacancies.json', 'r') as file:
            data = json.load(file)
            processed_vacancies.update(data)  # Добавление данных из файла в набор
    except FileNotFoundError:
        print("File 'processed_vacancies.json' not found")

    for geo_id in range(1, 11):  
        offset = 0
        total_vacancies = float('inf')
        while offset < total_vacancies:
            params = {
                'offset': offset,
                'limit': limit,
                'is_hidden': 0,
                'rubric_filter_mode': 'new',
                'geo_id': geo_id,
                'sort' : 'date'
            }
            
            req = requests.get(url=url, headers=headers, params=params)

            if req.status_code == 200:
                data = req.json()
                
                if data.get('vacancies'):
                    all_data['vacancies'].extend(data['vacancies'])
                    total_vacancies = data['metadata'].get('result_set', {}).get('count', total_vacancies)
                    for vacancy in data['vacancies']:
                        vacancy_id = vacancy.get('id')
                        if should_process_vacancy(vacancy_id, processed_vacancies):
                            mark_vacancy_as_processed(vacancy_id, processed_vacancies)
                    # Увеличиваем смещение для следующего запроса
                    offset += limit
                else:
                    print("The list of vacancies is empty")
                    break
            else:
                print(f"Error executing request: {req.status_code}\nurl: {url}, params: {params}")
                break
    
    extracted_data1 = []
    extracted_data2 = []

    for vacancy in all_data['vacancies']:
        full_url = vacancy.get('canonical_url', '')
        parsed_url = urlparse(full_url)
        domain = parsed_url.netloc
        vacancy_address = ''
        
        contact = vacancy.get('contact', {})
        if isinstance(contact, dict):
            name = contact.get('name', '')
            email = contact.get('email', '')
            phones = contact.get('phones', '')
            # if not phones or phones == []:
            #     continue
            vacancy_address = contact.get('address', '')
        else:
            pass# vacances.contact is empty => skip current vacancie ???
        
        vacancy_data1 = {
            'title': vacancy.get('header', ''),
            'name': name,
            'email': email,
            'phone': phones,
            'comment': full_url,
            'roistat_visit': domain,
            'fields': {
                'site' : domain,
                'source' : domain,
                'promocode': None
            }
        }

        vacancy_data2 = {
            'source': domain,
            'name': name,
            'email': email,
            'phone': phones,
            'data': (full_url, name, email, phones, vacancy_address)
        }
        extracted_data1.append(vacancy_data1)
        extracted_data2.append(vacancy_data2)
        
    with open('extracted_data1.json', 'w', encoding='utf-8') as file:
        json.dump(extracted_data1, file, ensure_ascii=False, indent=4)
    with open('extracted_data2.json', 'w', encoding='utf-8') as file:
        json.dump(extracted_data2, file, ensure_ascii=False, indent=4)
    save_processed_vacancies(processed_vacancies)

def send_webhook():
    with open('extracted_data1.json', 'r', encoding='utf-8') as file:
        json_data1 = json.load(file)
    with open('extracted_data2.json', 'r', encoding='utf-8') as file:
        json_data2 = json.load(file)
    webhook_url1 = 'https://cloud.roistat.com/integration/webhook?key=a58c86c38a259de63562d533d7c7edf4'
    webhook_url2 = 'https://c6ce863bb1eb.vps.myjino.ru/contacts?apiKey=Wy7RXAzSRZpD4a3q'
    time.sleep(2)
    req1 = requests.post(webhook_url1, json=json_data1)
    req2 = requests.post(webhook_url2, json=json_data2)

    print("Response from webhook1: ", req1.text)
    print("Response from webhook2: ", req2.text)
if __name__ == '__main__':
    req()
    #send_webhook()
    