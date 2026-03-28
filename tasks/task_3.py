import requests
import json
import os

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = 'resourse/save.json'
data = None
groups = {}

def load_groups():
    global groups
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                groups = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке файла: {e}")
            groups = {}
    else:
        groups = {}

def save_groups():
    global groups
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=2)
        print("Изменения сохранены.")
    except IOError as e:
        print(f"Ошибка при сохранении: {e}")

def fetch_currency_data():
    global data
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return True
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return False

def show_all_currencies():
    global data
    if not data:
        print("Нет данных. Обновите информацию.")
        return
    
    valute = data.get('Valute', {})
    print("\n" + "="*70)
    print(f"Курсы валют на {data.get('Date', 'Неизвестно')}\n")
    print(f"{'Код':<8} {'Валюта':<35} {'Курс (RUB)':<15} {'Номинал'}\n")
    
    for code, info in valute.items():
        print(f"{code:<8} {info['Name']:<35} {info['Value']:<15.4f} {info['Nominal']}")

def show_currency_by_code():
    global data
    if not data:
        print("Нет данных. Обновите информацию.")
        return
    
    code = input("Введите код валюты (например, USD, EUR): ").upper()
    valute = data.get('Valute', {})
    
    if code in valute:
        info = valute[code]
        print(f"\nКод: {code}")
        print(f"Валюта: {info['Name']}")
        print(f"Курс: {info['Value']:.4f} RUB")
        print(f"Номинал: {info['Nominal']} {info['Name']}\n")
    else:
        print(f"Валюта с кодом {code} не найдена.")

def create_group():
    global groups
    group_name = input("Введите название группы: ").strip()
    
    if not group_name:
        print("Название группы не может быть пустым.")
        return
    
    if group_name in groups:
        print(f"Группа '{group_name}' уже существует.")
        return
    
    groups[group_name] = []
    save_groups()
    print(f"Группа '{group_name}' успешно создана.")

def show_all_groups():
    global groups
    if not groups:
        print("Нет созданных групп.")
        return
    
    print("\nСозданные группы валют:\n")
    
    for group_name, currencies in groups.items():
        print(f"\n📁 {group_name}:")
        if currencies:
            for currency in currencies:
                print(f"   • {currency}")
        else:
            print("   (нет валют)")

def add_currency_to_group():
    global groups, data
    if not groups:
        print("Нет созданных групп. Сначала создайте группу.")
        return
    
    if not data:
        print("Нет данных о курсах валют. Обновите информацию.")
        return
    
    print("\nСуществующие группы:")
    groups_list = list(groups.keys())
    for i, group in enumerate(groups_list, 1):
        print(f"{i}, {group}")
    
    try:
        choice = int(input("\nВыберите номер группы: ")) - 1
        if 0 <= choice < len(groups_list):
            group_name = groups_list[choice]
        else:
            print("Неверный номер.")
            return
    except ValueError:
        print("Введите число.")
        return
    
    valute = data.get('Valute', {})
    print("\nДоступные валюты (первые 20):")
    available_currencies = list(valute.keys())
    for i, code in enumerate(available_currencies[:20], 1):
        print(f"{code} - {valute[code]['Name']}")
    
    currency_code = input("\nВведите код валюты: ").upper()
    
    if currency_code not in valute:
        print(f"Валюта с кодом {currency_code} не найдена.")
        return
    
    if currency_code in groups[group_name]:
        print(f"Валюта {currency_code} уже есть в группе.")
        return
    
    groups[group_name].append(currency_code)
    save_groups()
    print(f"Валюта {currency_code} добавлена в группу '{group_name}'.")

def edit_group_currencies():
    global groups, data
    if not groups:
        print("Нет созданных групп.")
        return
    
    if not data:
        print("Нет данных о курсах валют. Обновите информацию.")
        return
    
    print("\nСуществующие группы:")
    groups_list = list(groups.keys())
    for i, group in enumerate(groups_list, 1):
        print(f"{i}. {group}")
    
    try:
        choice = int(input("\nВыберите номер группы: ")) - 1
        if 0 <= choice < len(groups_list):
            group_name = groups_list[choice]
        else:
            print("Неверный номер.")
            return
    except ValueError:
        print("Введите число.")
        return
    
    while True:
        print(f"\n--- Редактирование группы '{group_name}' ---")
        print(f"Текущие валюты: {groups[group_name] if groups[group_name] else 'нет'}")
        print("\nВыберите действие:")
        print("1. Добавить валюту")
        print("2. Удалить валюту")
        print("3. Вернуться в главное меню")
        
        action = input("Ваш выбор: ").strip()
        
        if action == "1":
            valute = data.get('Valute', {})
            print("\nДоступные валюты (первые 20):")
            available_currencies = list(valute.keys())
            for i, code in enumerate(available_currencies[:20], 1):
                print(f"{i}. {code} - {valute[code]['Name']}")
            
            currency_code = input("\nВведите код валюты: ").upper()
            
            if currency_code not in valute:
                print(f"Валюта с кодом {currency_code} не найдена.")
                continue
            
            if currency_code in groups[group_name]:
                print(f"Валюта {currency_code} уже есть в группе.")
            else:
                groups[group_name].append(currency_code)
                save_groups()
                print(f"Валюта {currency_code} добавлена.")
        
        elif action == "2":
            if not groups[group_name]:
                print("В группе нет валют для удаления.")
                continue
            
            print(f"\nВалюты в группе '{group_name}':")
            for i, currency in enumerate(groups[group_name], 1):
                print(f"{currency}")
            
            try:
                del_choice = int(input("\nВыберите номер валюты для удаления: ")) - 1
                if 0 <= del_choice < len(groups[group_name]):
                    removed = groups[group_name].pop(del_choice)
                    save_groups()
                    print(f"Валюта {removed} удалена из группы.")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число.")
        
        elif action == "3":
            break
        
        else:
            print("Неверный выбор.")

def show_group_currencies_rate():
    global groups, data
    if not groups:
        print("Нет созданных групп.")
        return
    
    if not data:
        print("Нет данных о курсах валют. Обновите информацию.")
        return
    
    print("\nСуществующие группы:")
    groups_list = list(groups.keys())
    for i, group in enumerate(groups_list, 1):
        print(f"{i}. {group}")
    
    try:
        choice = int(input("\nВыберите номер группы: ")) - 1
        if 0 <= choice < len(groups_list):
            group_name = groups_list[choice]
        else:
            print("Неверный номер.")
            return
    except ValueError:
        print("Введите число.")
        return
    
    currencies = groups[group_name]
    if not currencies:
        print(f"В группе '{group_name}' нет валют.")
        return
    
    valute = data.get('Valute', {})
    print(f"\nКурсы валют в группе '{group_name}':\n")
    print(f"{'Код':<8} {'Валюта':<35} {'Курс (RUB)':<15}\n")
    
    for code in currencies:
        if code in valute:
            info = valute[code]
            print(f"{code:<8} {info['Name']:<35} {info['Value']:<15.4f}")
        else:
            print(f"{code:<8} {'Не найдена':<35} {'-':<15}")

def main_menu():
    load_groups()
    
    while True:
        print("\nКУРСЫ ВАЛЮТ - ГЛАВНОЕ МЕНЮ\n")
        print("1. Обновить данные о курсах валют")
        print("2. Показать все валюты")
        print("3. Найти валюту по коду")
        print("4. Создать новую группу")
        print("5. Показать все группы")
        print("6. Добавить валюту в группу")
        print("7. Редактировать группу (добавить/удалить валюту)")
        print("8. Показать курсы валют из группы")
        print("0. Выход\n")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            if fetch_currency_data():
                print("Данные успешно обновлены!")
        
        elif choice == "2":
            show_all_currencies()
        
        elif choice == "3":
            show_currency_by_code()
        
        elif choice == "4":
            create_group()
        
        elif choice == "5":
            show_all_groups()
        
        elif choice == "6":
            add_currency_to_group()
        
        elif choice == "7":
            edit_group_currencies()
        
        elif choice == "8":
            show_group_currencies_rate()
        
        elif choice == "0":
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main_menu()