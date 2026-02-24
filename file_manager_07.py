"""
Консольный файловый менеджер
Версия 2.0 с сохранением данных и экспортом содержимого
"""
import os
import shutil
import platform
import sys
from datetime import datetime
import json

# Глобальная переменная для рабочей директории
working_directory = os.getcwd()

# Константы для файлов с данными
BANK_ACCOUNT_FILE = "bank_account.json"
LISTDIR_FILE = "listdir.txt"

def clear_screen():
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Вывод заголовка"""
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

def wait_for_enter():
    """Ожидание нажатия Enter"""
    input("\nНажмите Enter для продолжения...")

def show_menu():
    """Отображение главного меню"""
    clear_screen()
    print_header("КОНСОЛЬНЫЙ ФАЙЛОВЫЙ МЕНЕДЖЕР")
    print(f"Текущая директория: {working_directory}")
    print("=" * 60)
    print("1. Создать папку")
    print("2. Удалить (файл/папку)")
    print("3. Копировать (файл/папку)")
    print("4. Просмотр содержимого рабочей директории")
    print("5. Посмотреть только папки")
    print("6. Посмотреть только файлы")
    print("7. Просмотр информации об операционной системе")
    print("8. Создатель программы")
    print("9. Играть в викторину")
    print("10. Мой банковский счет")
    print("11. Смена рабочей директории")
    print("12. Сохранить содержимое директории в файл")  # Новый пункт
    print("13. Выход")
    print("=" * 60)
    return input("Выберите пункт меню: ")

# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ ==========

def create_folder():
    """Создание папки в рабочей директории"""
    clear_screen()
    print_header("СОЗДАНИЕ ПАПКИ")
    folder_name = input("Введите название папки: ").strip()
    
    if not folder_name:
        print("Ошибка: Название папки не может быть пустым!")
        wait_for_enter()
        return
    
    folder_path = os.path.join(working_directory, folder_name)
    
    try:
        os.makedirs(folder_path, exist_ok=False)
        print(f"Папка '{folder_name}' успешно создана!")
    except FileExistsError:
        print(f"Ошибка: Папка '{folder_name}' уже существует!")
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")
    
    wait_for_enter()

def delete_item():
    """Удаление файла или папки"""
    clear_screen()
    print_header("УДАЛЕНИЕ")
    item_name = input("Введите название файла или папки для удаления: ").strip()
    
    if not item_name:
        print("Ошибка: Имя не может быть пустым!")
        wait_for_enter()
        return
    
    item_path = os.path.join(working_directory, item_name)
    
    if not os.path.exists(item_path):
        print(f"Ошибка: '{item_name}' не найден!")
        wait_for_enter()
        return
    
    # Подтверждение удаления
    confirm = input(f"Вы уверены, что хотите удалить '{item_name}'? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Удаление отменено.")
        wait_for_enter()
        return
    
    try:
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Файл '{item_name}' успешно удален!")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Папка '{item_name}' успешно удалена!")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    
    wait_for_enter()

def copy_item():
    """Копирование файла или папки"""
    clear_screen()
    print_header("КОПИРОВАНИЕ")
    source_name = input("Введите название исходного файла/папки: ").strip()
    
    if not source_name:
        print("Ошибка: Имя не может быть пустым!")
        wait_for_enter()
        return
    
    source_path = os.path.join(working_directory, source_name)
    
    if not os.path.exists(source_path):
        print(f"Ошибка: '{source_name}' не найден!")
        wait_for_enter()
        return
    
    dest_name = input("Введите новое название (для копии): ").strip()
    
    if not dest_name:
        print("Ошибка: Новое имя не может быть пустым!")
        wait_for_enter()
        return
    
    dest_path = os.path.join(working_directory, dest_name)
    
    if os.path.exists(dest_path):
        print(f"Ошибка: '{dest_name}' уже существует!")
        wait_for_enter()
        return
    
    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"Файл '{source_name}' скопирован в '{dest_name}'!")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path)
            print(f"Папка '{source_name}' скопирована в '{dest_name}'!")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
    
    wait_for_enter()

def list_contents():
    """Просмотр всего содержимого рабочей директории"""
    clear_screen()
    print_header("СОДЕРЖИМОЕ ДИРЕКТОРИИ")
    
    try:
        items = os.listdir(working_directory)
        if not items:
            print("Директория пуста")
        else:
            files = []
            dirs = []
            
            for item in sorted(items):
                item_path = os.path.join(working_directory, item)
                if os.path.isfile(item_path):
                    files.append(item)
                else:
                    dirs.append(item)
            
            print("ФАЙЛЫ:")
            for i, file in enumerate(files, 1):
                file_path = os.path.join(working_directory, file)
                size = os.path.getsize(file_path)
                print(f"{i:3}. 📄 {file} ({size} байт)")
            
            print("\nПАПКИ:")
            for i, dir_name in enumerate(dirs, 1):
                print(f"{i:3}. 📁 {dir_name}")
    except Exception as e:
        print(f"Ошибка при чтении директории: {e}")
    
    wait_for_enter()

def list_folders():
    """Просмотр только папок"""
    clear_screen()
    print_header("ТОЛЬКО ПАПКИ")
    
    try:
        items = os.listdir(working_directory)
        folders = [item for item in items if os.path.isdir(os.path.join(working_directory, item))]
        
        if not folders:
            print("Папки не найдены")
        else:
            for i, folder in enumerate(sorted(folders), 1):
                print(f"{i:3}. 📁 {folder}")
    except Exception as e:
        print(f"Ошибка при чтении директории: {e}")
    
    wait_for_enter()

def list_files():
    """Просмотр только файлов"""
    clear_screen()
    print_header("ТОЛЬКО ФАЙЛЫ")
    
    try:
        items = os.listdir(working_directory)
        files = [item for item in items if os.path.isfile(os.path.join(working_directory, item))]
        
        if not files:
            print("Файлы не найдены")
        else:
            for i, file in enumerate(sorted(files), 1):
                file_path = os.path.join(working_directory, file)
                size = os.path.getsize(file_path)
                print(f"{i:3}. 📄 {file} ({size} байт)")
    except Exception as e:
        print(f"Ошибка при чтении директории: {e}")
    
    wait_for_enter()

def save_directory_contents():
    """Сохранение содержимого директории в файл"""
    clear_screen()
    print_header("СОХРАНЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ")
    
    try:
        items = os.listdir(working_directory)
        files = []
        dirs = []
        
        for item in sorted(items):
            item_path = os.path.join(working_directory, item)
            if os.path.isfile(item_path):
                files.append(item)
            else:
                dirs.append(item)
        
        # Создаем содержимое для файла
        content = []
        content.append("files:")
        for file in files:
            content.append(file)
        
        content.append("\ndirs:")
        for dir_name in dirs:
            content.append(dir_name)
        
        # Записываем в файл
        file_path = os.path.join(working_directory, LISTDIR_FILE)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"Содержимое успешно сохранено в файл: {LISTDIR_FILE}")
        print(f"Найдено файлов: {len(files)}, папок: {len(dirs)}")
        
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
    
    wait_for_enter()

def system_info():
    """Информация об операционной системе"""
    clear_screen()
    print_header("ИНФОРМАЦИЯ О СИСТЕМЕ")
    
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Версия: {platform.version()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Имя компьютера: {platform.node()}")
    print(f"Пользователь: {os.getenv('USERNAME') or os.getenv('USER') or 'Неизвестно'}")
    print(f"Текущее время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    wait_for_enter()

def show_creator():
    """Информация о создателе программы"""
    clear_screen()
    print_header("СОЗДАТЕЛЬ ПРОГРАММЫ")
    
    print("""
    ╔══════════════════════════════════════════╗
    ║   Консольный файловый менеджер v2.0      ║
    ║                                          ║
    ║   Разработчик: Bertek                    ║
    ║   Дата создания: 2026                    ║
    ║   Курс: Основы программирования на Python║
    ║                                          ║
    ║   Новое:                                 ║
    ║   ✓ Сохранение банковского счета в JSON  ║
    ║   ✓ Экспорт содержимого в listdir.txt    ║
    ║   ✓ История покупок сохраняется          ║
    ╚══════════════════════════════════════════╝
    """)
    
    wait_for_enter()

# ========== ИГРА ВИКТОРИНА ==========

def play_quiz():
    """Игра викторина"""
    clear_screen()
    print_header("ВИКТОРИНА")
    
    questions = [
        {
            "question": "Столица Франции?",
            "options": ["1. Лондон", "2. Берлин", "3. Париж", "4. Мадрид"],
            "answer": 3
        },
        {
            "question": "Сколько планет в Солнечной системе?",
            "options": ["1. 7", "2. 8", "3. 9", "4. 10"],
            "answer": 2
        },
        {
            "question": "Кто написал 'Войну и мир'?",
            "options": ["1. Достоевский", "2. Толстой", "3. Пушкин", "4. Чехов"],
            "answer": 2
        },
        {
            "question": "Какой язык программирования мы изучаем?",
            "options": ["1. Java", "2. C++", "3. Python", "4. JavaScript"],
            "answer": 3
        },
        {
            "question": "Сколько байт в килобайте?",
            "options": ["1. 1000", "2. 1024", "3. 2048", "4. 512"],
            "answer": 2
        }
    ]
    
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions, 1):
        print(f"\nВопрос {i}/{total}: {q['question']}")
        for option in q['options']:
            print(option)
        
        try:
            answer = int(input("Ваш ответ (номер варианта): "))
            if answer == q['answer']:
                print("✅ Правильно!")
                score += 1
            else:
                correct_option = q['options'][q['answer'] - 1][3:]
                print(f"❌ Неправильно! Правильный ответ: {correct_option}")
        except ValueError:
            print("❌ Некорректный ввод!")
    
    print(f"\nРезультат: {score}/{total} правильных ответов ({score/total*100:.1f}%)")
    wait_for_enter()

# ========== БАНКОВСКИЙ СЧЕТ (ОБНОВЛЕННАЯ ВЕРСИЯ) ==========

def load_bank_data():
    """Загрузка данных банковского счета из JSON файла"""
    if os.path.exists(BANK_ACCOUNT_FILE):
        try:
            with open(BANK_ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('balance', 0.0), data.get('purchases', [])
        except (json.JSONDecodeError, IOError):
            return 0.0, []
    return 0.0, []

def save_bank_data(balance, purchases):
    """Сохранение данных банковского счета в JSON файл"""
    try:
        data = {
            'balance': balance,
            'purchases': purchases,
            'last_updated': datetime.now().isoformat()
        }
        with open(BANK_ACCOUNT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def bank_account():
    """Управление банковским счетом с сохранением в JSON"""
    balance, purchases = load_bank_data()
    
    while True:
        clear_screen()
        print_header("МОЙ БАНКОВСКИЙ СЧЕТ")
        print(f"Текущий баланс: {balance:.2f} руб.")
        print(f"Всего покупок: {len(purchases)}")
        print("-" * 60)
        print("1. Пополнить счет")
        print("2. Совершить покупку")
        print("3. История покупок")
        print("4. Очистить историю")
        print("5. Выход в главное меню")
        print("-" * 60)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            try:
                amount = float(input("Введите сумму пополнения: "))
                if amount > 0:
                    balance += amount
                    print(f"✅ Счет пополнен на {amount:.2f} руб.")
                    save_bank_data(balance, purchases)
                else:
                    print("❌ Сумма должна быть положительной!")
            except ValueError:
                print("❌ Некорректная сумма!")
        
        elif choice == "2":
            try:
                amount = float(input("Введите стоимость покупки: "))
                if amount <= 0:
                    print("❌ Стоимость должна быть положительной!")
                    continue
                
                if amount > balance:
                    print("❌ Недостаточно средств!")
                    continue
                
                purchase_name = input("Введите название покупки: ").strip()
                if not purchase_name:
                    purchase_name = "Покупка"
                
                balance -= amount
                purchase_record = {
                    'name': purchase_name,
                    'amount': amount,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'balance_after': balance
                }
                purchases.append(purchase_record)
                
                if save_bank_data(balance, purchases):
                    print(f"✅ Покупка совершена!")
                else:
                    print("⚠️ Покупка совершена, но данные не сохранены!")
                
            except ValueError:
                print("❌ Некорректная сумма!")
        
        elif choice == "3":
            clear_screen()
            print_header("ИСТОРИЯ ПОКУПОК")
            if purchases:
                total_spent = sum(p['amount'] for p in purchases)
                print(f"Всего потрачено: {total_spent:.2f} руб.\n")
                
                for i, purchase in enumerate(purchases, 1):
                    print(f"{i}. {purchase['date']}")
                    print(f"   {purchase['name']} - {purchase['amount']:.2f} руб.")
                    print(f"   Баланс после: {purchase['balance_after']:.2f} руб.\n")
            else:
                print("История покупок пуста")
            wait_for_enter()
            continue
        
        elif choice == "4":
            confirm = input("Вы уверены, что хотите очистить историю? (y/n): ").strip().lower()
            if confirm == 'y':
                purchases = []
                if save_bank_data(balance, purchases):
                    print("✅ История очищена!")
                else:
                    print("❌ Ошибка при сохранении!")
            wait_for_enter()
        
        elif choice == "5":
            if save_bank_data(balance, purchases):
                print("✅ Данные сохранены!")
            else:
                print("❌ Ошибка сохранения данных!")
            wait_for_enter()
            break
        
        else:
            print("❌ Неверный пункт меню!")
        
        if choice in ["1", "2", "4"]:
            wait_for_enter()

# ========== СМЕНА РАБОЧЕЙ ДИРЕКТОРИИ ==========

def change_directory():
    """Смена рабочей директории"""
    global working_directory
    
    clear_screen()
    print_header("СМЕНА РАБОЧЕЙ ДИРЕКТОРИИ")
    print(f"Текущая директория: {working_directory}")
    print("\nПодсказки:")
    print("  • Абсолютный путь: C:/Users/User/Documents или /home/user/Documents")
    print("  • Относительный путь: user/my/ или .. (родительская папка)")
    print("  • '.' - текущая папка")
    print("-" * 60)
    
    new_path = input("Введите новый путь: ").strip()
    
    if not new_path:
        print("❌ Путь не может быть пустым!")
        wait_for_enter()
        return
    
    # Проверяем, не является ли путь абсолютным
    if os.path.isabs(new_path):
        target_path = new_path
    else:
        # Относительный путь от текущей директории
        target_path = os.path.join(working_directory, new_path)
    
    # Нормализуем путь
    target_path = os.path.normpath(target_path)
    
    if os.path.exists(target_path) and os.path.isdir(target_path):
        working_directory = target_path
        print(f"✅ Рабочая директория изменена на:\n{working_directory}")
    else:
        print(f"❌ Путь не существует или не является папкой!")
    
    wait_for_enter()

# ========== ГЛАВНАЯ ПРОГРАММА ==========

def main():
    """Главная функция программы"""
    global working_directory
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            create_folder()
        elif choice == "2":
            delete_item()
        elif choice == "3":
            copy_item()
        elif choice == "4":
            list_contents()
        elif choice == "5":
            list_folders()
        elif choice == "6":
            list_files()
        elif choice == "7":
            system_info()
        elif choice == "8":
            show_creator()
        elif choice == "9":
            play_quiz()
        elif choice == "10":
            bank_account()
        elif choice == "11":
            change_directory()
        elif choice == "12":
            save_directory_contents()
        elif choice == "13":
            clear_screen()
            print("Спасибо за использование программы! До свидания!")
            sys.exit(0)
        else:
            print("❌ Неверный пункт меню! Пожалуйста, выберите 1-13.")
            wait_for_enter()

if __name__ == "__main__":
    main()
