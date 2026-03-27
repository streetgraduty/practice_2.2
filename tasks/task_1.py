import requests

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

print(f"{'URL':<40} {'Статус':<20} {'Код ответа':<10}")

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        code = response.status_code
        
        if code == 200:
            status = "доступен"
        elif code == 404:
            status = "не найден"
        elif code == 403:
            status = "вход запрещен"
        elif code >= 500:
            status = "не доступен"
        else:
            if 200 <= code < 400:
                status = "доступен"
            else:
                status = "не доступен"

    except requests.exceptions.RequestException:
        status = "не доступен"
        code = "—"
    
    print(f"{url:<40} {status:<20} {code:<10}")
    
urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

print(f"{'URL':<40} {'Статус':<20} {'Код ответа':<10}")

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        code = response.status_code