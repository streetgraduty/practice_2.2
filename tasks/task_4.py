import requests

BASE_URL = "https://api.github.com"

def get_user_profile(username):
    try:
        response = requests.get(f"{BASE_URL}/users/{username}")
        
        if response.status_code == 404:
            print(f"Пользователь '{username}' не найден.")
            return False
        elif response.status_code != 200:
            print(f"Ошибка при получении данных. Код: {response.status_code}")
            return False
        
        user_data = response.json()
        
        print(f"\nПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ: {user_data.get('login', 'N/A')}")
        print(f"\nИмя: {user_data.get('name', 'Не указано')}")
        print(f"Ссылка на профиль: {user_data.get('html_url', 'N/A')}")
        print(f"Количество репозиториев: {user_data.get('public_repos', 0)}")
        print(f"Количество подписчиков: {user_data.get('followers', 0)}")
        print(f"Количество подписок: {user_data.get('following', 0)}")
        print(f"Биография: {user_data.get('bio', 'Не указана')}\n")
        
        return True
        
    except requests.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return False

def get_user_repos(username):
    try:
        response = requests.get(f"{BASE_URL}/users/{username}/repos", 
                               params={"per_page": 100, "sort": "updated"})
        
        if response.status_code == 404:
            print(f"Пользователь '{username}' не найден.")
            return False
        elif response.status_code != 200:
            print(f"Ошибка при получении данных. Код: {response.status_code}")
            return False
        
        repos = response.json()
        
        if not repos:
            print(f"У пользователя '{username}' нет публичных репозиториев.")
            return True
        
        print(f"\nРЕПОЗИТОРИИ ПОЛЬЗОВАТЕЛЯ: {username}\n")
        
        for repo in repos:
            print(f"\n{repo.get('name', 'N/A')}")
            print(f"   Ссылка: {repo.get('html_url', 'N/A')}")
            print(f"   Описание: {repo.get('description', 'Нет описания')}")
            print(f"   Язык: {repo.get('language', 'Не указан')}")
            print(f"   Видимость: {'Публичный' if not repo.get('private') else 'Приватный'}")
            print(f"   Ветка по умолчанию: {repo.get('default_branch', 'N/A')}")
            print(f"   Звёзды: {repo.get('stargazers_count', 0)}\n")
        
        print(f"\nВсего репозиториев: {len(repos)}")
        return True
        
    except requests.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return False

def search_repositories(query):
    try:
        response = requests.get(f"{BASE_URL}/search/repositories", 
                               params={"q": query, "per_page": 10, "sort": "stars"})
        
        if response.status_code != 200:
            print(f"Ошибка при поиске. Код: {response.status_code}")
            return False
        
        search_data = response.json()
        repos = search_data.get('items', [])
        
        if not repos:
            print(f"По запросу '{query}' ничего не найдено.")
            return True
        
        print(f"\nРЕЗУЛЬТАТЫ ПОИСКА: {query}")
        print(f"Найдено репозиториев: {search_data.get('total_count', 0)}\n")
        
        for i, repo in enumerate(repos, 1):
            print(f"\n{i}. {repo.get('name', 'N/A')}")
            print(f"   Владелец: {repo.get('owner', {}).get('login', 'N/A')}")
            print(f"   Ссылка: {repo.get('html_url', 'N/A')}")
            print(f"   Описание: {repo.get('description', 'Нет описания')}")
            print(f"   Язык: {repo.get('language', 'Не указан')}")
            print(f"   Звёзды: {repo.get('stargazers_count', 0)}")
            print("-"*50)
        
        return True
        
    except requests.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return False

def main_menu():
    while True:
        print("1. Просмотреть профиль пользователя")
        print("2. Показать все репозитории пользователя")
        print("3. Найти репозитории по названию")
        print("0. Выход\n")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            username = input("Введите имя пользователя GitHub: ").strip()
            if username:
                get_user_profile(username)
            else:
                print("Имя пользователя не может быть пустым.")
        
        elif choice == "2":
            username = input("Введите имя пользователя GitHub: ").strip()
            if username:
                get_user_repos(username)
            else:
                print("Имя пользователя не может быть пустым")
        
        elif choice == "3":
            query = input("Введите название репозитория для поиска: ").strip()
            if query:
                search_repositories(query)
            else:
                print("Название для поиска не может быть пустым")
        
        elif choice == "0":
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()