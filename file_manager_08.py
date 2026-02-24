"""
Консольный файловый менеджер
Версия 2.1 с улучшенным кодом (генераторы, тернарные операторы, декораторы)
"""
import os
import shutil
import platform
import sys
from datetime import datetime
import json
from functools import wraps
from typing import List, Tuple, Any, Callable

# Глобальная переменная для рабочей директории
working_directory = os.getcwd()

# Константы для файлов с данными
BANK_ACCOUNT_FILE = "bank_account.json"
LISTDIR_FILE = "listdir.txt"

# ========== ДЕКОРАТОРЫ ==========

def error_handler(func: Callable) -> Callable:
    """Декоратор для обработки ошибок в функциях"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n⚠️ Операция прервана пользователем")
            wait_for_enter()
        except Exception as e:
            print(f"❌ Ошибка в {func.__name__}: {e}")
            wait_for_enter()
    return wrapper

def confirm_action(message: str = "Вы уверены? (y/n): ") -> Callable:
    """Декоратор для подтверждения действия"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirm = input(message).strip().lower()
            return func(*args, **kwargs) if confirm == 'y' else print("Действие отменено.")
        return wrapper
    return decorator

def log_action(func: Callable) -> Callable:
    """Декоратор для логирования действий"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Выполнено: {func.__name__}")
        return result
    return wrapper

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def clear_screen() -> None:
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str) -> None:
    """Вывод заголовка"""
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

def wait_for_enter() -> None:
    """Ожидание нажатия Enter"""
    input("\nНажмите Enter для продолжения...")

def get_directory_items() -> Tuple[List[str], List[str]]:
    """Генератор для получения файлов и папок"""
    try:
        items = os.listdir(working_directory)
        # Используем генераторы для разделения файлов и папок
        files = (item for item in items if os.path.isfile(os.path.join(working_directory, item)))
        dirs = (item for item in items if os.path.isdir(os.path.join(working_directory, item)))
        return sorted(files), sorted(dirs)
    except PermissionError:
        print("❌ Нет прав доступа к директории")
        return [], []
    except Exception as e:
        print(f"❌ Ошибка при чтении директории: {e}")
        return [], []

@error_handler
def show_menu() -> str:
    """Отображение главного меню"""
    clear_screen()
    print_header("КОНСОЛЬНЫЙ ФАЙЛОВЫЙ МЕНЕДЖЕР")
    print(f"Текущая директория: {working_directory}")
    print("=" * 60)
    
    menu_items = [
        "1. Создать папку",
        "2. Удалить (файл/папку)",
        "3. Копировать (файл/папку)",
        "4. Просмотр содержимого рабочей директории",
        "5. Посмотреть только папки",
        "6. Посмотреть только файлы",
        "7. Просмотр информации об операционной системе",
        "8. Создатель программы",
        "9. Играть в викторину",
        "10. Мой банковский счет",
        "11. Смена рабочей директории",
        "12. Сохранить содержимое директории в файл",
        "13. Выход"
    ]
    
    # Используем генератор для вывода меню
    print('\n'.join(menu_items))
    print("=" * 60)
    
    return input("Выберите пункт меню: ").strip()

# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ ==========

@error_handler
@log_action
def create_folder() -> None:
    """Создание папки в рабочей директории"""
    clear_screen()
    print_header("СОЗДАНИЕ ПАПКИ")
    
    folder_name = input("Введите название папки: ").strip()
    
    # Тернарный оператор для проверки пустого имени
    print("Ошибка: Название папки не может быть пустым!") if not folder_name else None
    
    if not folder_name:
        wait_for_enter()
        return
    
    folder_path = os.path.join(working_directory, folder_name)
    
    try:
        os.makedirs(folder_path, exist_ok=False)
        print(f"✅ Папка '{folder_name}' успешно создана!")
    except FileExistsError:
        print(f"❌ Ошибка: Папка '{folder_name}' уже существует!")
    
    wait_for_enter()

@error_handler
@confirm_action("Вы уверены, что хотите удалить? (y/n): ")
@log_action
def delete_item() -> None:
    """Удаление файла или папки"""
    clear_screen()
    print_header("УДАЛЕНИЕ")
    
    item_name = input("Введите название файла или папки для удаления: ").strip()
    
    if not item_name:
        print("❌ Ошибка: Имя не может быть пустым!")
        wait_for_enter()
        return
    
    item_path = os.path.join(working_directory, item_name)
    
    if not os.path.exists(item_path):
        print(f"❌ Ошибка: '{item_name}' не найден!")
        wait_for_enter()
        return
    
    try:
        # Тернарный оператор для выбора метода удаления
        os.remove(item_path) if os.path.isfile(item_path) else shutil.rmtree(item_path)
        print(f"✅ '{item_name}' успешно удален!")
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")
    
    wait_for_enter()

@error_handler
@log_action
def copy_item() -> None:
    """Копирование файла или папки"""
    clear_screen()
    print_header("КОПИРОВАНИЕ")
    
    source_name = input("Введите название исходного файла/папки: ").strip()
    dest_name = input("Введите новое название (для копии): ").strip()
    
    # Проверка с использованием тернарных операторов
    errors = []
    errors.append("❌ Имя исходного файла не может быть пустым!") if not source_name else None
    errors.append("❌ Новое имя не может быть пустым!") if not dest_name else None
    
    if errors:
        print('\n'.join(errors))
        wait_for_enter()
        return
    
    source_path = os.path.join(working_directory, source_name)
    dest_path = os.path.join(working_directory, dest_name)
    
    if not os.path.exists(source_path):
        print(f"❌ Ошибка: '{source_name}' не найден!")
        wait_for_enter()
        return
    
    if os.path.exists(dest_path):
        print(f"❌ Ошибка: '{dest_name}' уже существует!")
        wait_for_enter()
        return
    
    try:
        # Тернарный оператор для выбора метода копирования
        (shutil.copy2 if os.path.isfile(source_path) else shutil.copytree)(source_path, dest_path)
        print(f"✅ '{source_name}' скопирован в '{dest_name}'!")
    except Exception as e:
        print(f"❌ Ошибка при копировании: {e}")
    
    wait_for_enter()

@error_handler
def list_contents() -> None:
    """Просмотр всего содержимого рабочей директории"""
    clear_screen()
    print_header("СОДЕРЖИМОЕ ДИРЕКТОРИИ")
    
    files, dirs = get_directory_items()
    
    # Используем тернарный оператор и генераторы для вывода
    print("ФАЙЛЫ:" if files else "ФАЙЛЫ не найдены")
    if files:
        # Генератор для вывода файлов с размерами
        file_list = (f"{i:3}. 📄 {file} ({os.path.getsize(os.path.join(working_directory, file))} байт)" 
                    for i, file in enumerate(files, 1))
        print('\n'.join(file_list))
    
    print("\nПАПКИ:" if dirs else "\nПАПКИ не найдены")
    if dirs:
        # Генератор для вывода папок
        dir_list = (f"{i:3}. 📁 {dir_name}" for i, dir_name in enumerate(dirs, 1))
        print('\n'.join(dir_list))
    
    wait_for_enter()

@error_handler
def list_folders() -> None:
    """Просмотр только папок"""
    clear_screen()
    print_header("ТОЛЬКО ПАПКИ")
    
    _, dirs = get_directory_items()
    
    # Тернарный оператор для вывода
    print("Папки не найдены" if not dirs else '\n'.join(
        f"{i:3}. 📁 {folder}" for i, folder in enumerate(dirs, 1)
    ))
    
    wait_for_enter()

@error_handler
def list_files() -> None:
    """Просмотр только файлов"""
    clear_screen()
    print_header("ТОЛЬКО ФАЙЛЫ")
    
    files, _ = get_directory_items()
    
    # Тернарный оператор с генератором
    print("Файлы не найдены" if not files else '\n'.join(
        f"{i:3}. 📄 {file} ({os.path.getsize(os.path.join(working_directory, file))} байт)" 
        for i, file in enumerate(files, 1)
    ))
    
    wait_for_enter()

@error_handler
@log_action
def save_directory_contents() -> None:
    """Сохранение содержимого директории в файл"""
    clear_screen()
    print_header("СОХРАНЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ")
    
    files, dirs = get_directory_items()
    
    # Генераторы для создания содержимого файла
    content_parts = []
    content_parts.append("files:")
    content_parts.extend(files)
    content_parts.append("\ndirs:")
    content_parts.extend(dirs)
    
    try:
        file_path = os.path.join(working_directory, LISTDIR_FILE)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        
        print(f"✅ Содержимое сохранено в файл: {LISTDIR_FILE}")
        print(f"Найдено файлов: {len(files)}, папок: {len(dirs)}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
    
    wait_for_enter()

@error_handler
def system_info() -> None:
    """Информация об операционной системе"""
    clear_screen()
    print_header("ИНФОРМАЦИЯ О СИСТЕМЕ")
    
    info_items = [
        f"Операционная система: {platform.system()} {platform.release()}",
        f"Версия: {platform.version()}",
        f"Архитектура: {platform.machine()}",
        f"Процессор: {platform.processor()}",
        f"Имя компьютера: {platform.node()}",
        f"Пользователь: {os.getenv('USERNAME') or os.getenv('USER') or 'Неизвестно'}",
        f"Текущее время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    # Генератор для вывода информации
    print('\n'.join(info_items))
    wait_for_enter()

def show_creator() -> None:
    """Информация о создателе программы"""
    clear_screen()
    print_header("СОЗДАТЕЛЬ ПРОГРАММЫ")
    
    creator_info = """
    ╔══════════════════════════════════════════╗
    ║   Консольный файловый менеджер v2.1      ║
    ║                                          ║
    ║   Разработчик: Bertek                    ║
    ║   Дата создания: 2026                    ║
    ║   Курс: Основы программирования на Python║
    ║                                          ║
    ║   Улучшения:                             ║
    ║   ✓ Генераторы и тернарные операторы     ║
    ║   ✓ Декораторы для обработки ошибок      ║
    ║   ✓ Улучшенная обработка исключений      ║
    ╚══════════════════════════════════════════╝
    """
    
    print(creator_info)
    wait_for_enter()

# ========== ИГРА ВИКТОРИНА ==========

@error_handler
def play_quiz() -> None:
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
    
    # Генератор для подсчета очков
    scores = []
    for q in questions:
        print(f"\n{q['question']}")
        print('\n'.join(q['options']))
        
        try:
            answer = int(input("Ваш ответ (номер варианта): "))
            is_correct = answer == q['answer']
            scores.append(is_correct)
            
            # Тернарный оператор для вывода результата
            print("✅ Правильно!" if is_correct else f"❌ Неправильно! Правильный ответ: {q['options'][q['answer'] - 1][3:]}")
        except ValueError:
            print("❌ Некорректный ввод!")
            scores.append(False)
    
    total = len(scores)
    correct = sum(scores)
    print(f"\nРезультат: {correct}/{total} правильных ответов ({correct/total*100:.1f}%)")
    wait_for_enter()

# ========== БАНКОВСКИЙ СЧЕТ ==========

@error_handler
def load_bank_data() -> Tuple[float, List[dict]]:
    """Загрузка данных банковского счета из JSON файла"""
    try:
        with open(BANK_ACCOUNT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('balance', 0.0), data.get('purchases', [])
    except FileNotFoundError:
        return 0.0, []
    except json.JSONDecodeError:
        print("⚠️ Файл поврежден, создаем новый")
        return 0.0, []
    except Exception as e:
        print(f"⚠️ Ошибка загрузки: {e}")
        return 0.0, []

@error_handler
def save_bank_data(balance: float, purchases: List[dict]) -> bool:
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

@error_handler
def bank_account() -> None:
    """Управление банковским счетом с сохранением в JSON"""
    balance, purchases = load_bank_data()
    
    while True:
        clear_screen()
        print_header("МОЙ БАНКОВСКИЙ СЧЕТ")
        print(f"Текущий баланс: {balance:.2f} руб.")
        print(f"Всего покупок: {len(purchases)}")
        print("-" * 60)
        
        menu_options = [
            "1. Пополнить счет",
            "2. Совершить покупку",
            "3. История покупок",
            "4. Очистить историю",
            "5. Выход в главное меню"
        ]
        print('\n'.join(menu_options))
        print("-" * 60)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            try:
                amount = float(input("Введите сумму пополнения: "))
                # Тернарный оператор для проверки суммы
                balance += amount if amount > 0 else print("❌ Сумма должна быть положительной!") or 0
                if amount > 0:
                    print(f"✅ Счет пополнен на {amount:.2f} руб.")
                    save_bank_data(balance, purchases)
            except ValueError:
                print("❌ Некорректная сумма!")
        
        elif choice == "2":
            try:
                amount = float(input("Введите стоимость покупки: "))
                purchase_name = input("Введите название покупки: ").strip() or "Покупка"
                
                # Проверки с использованием тернарных операторов
                if amount <= 0:
                    print("❌ Стоимость должна быть положительной!")
                elif amount > balance:
                    print("❌ Недостаточно средств!")
                else:
                    balance -= amount
                    purchase_record = {
                        'name': purchase_name,
                        'amount': amount,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'balance_after': balance
                    }
                    purchases.append(purchase_record)
                    save_bank_data(balance, purchases)
                    print(f"✅ Покупка совершена!")
            except ValueError:
                print("❌ Некорректная сумма!")
        
        elif choice == "3":
            clear_screen()
            print_header("ИСТОРИЯ ПОКУПОК")
            if purchases:
                total_spent = sum(p['amount'] for p in purchases)
                print(f"Всего потрачено: {total_spent:.2f} руб.\n")
                
                # Генератор для вывода истории
                purchase_history = (
                    f"{i}. {p['date']}\n   {p['name']} - {p['amount']:.2f} руб.\n   Баланс после: {p['balance_after']:.2f} руб.\n"
                    for i, p in enumerate(purchases, 1)
                )
                print(''.join(purchase_history))
            else:
                print("История покупок пуста")
            wait_for_enter()
            continue
        
        elif choice == "4":
            if input("Вы уверены, что хотите очистить историю? (y/n): ").strip().lower() == 'y':
                purchases = []
                save_bank_data(balance, purchases)
                print("✅ История очищена!")
            wait_for_enter()
        
        elif choice == "5":
            save_bank_data(balance, purchases)
            print("✅ Данные сохранены!" if save_bank_data(balance, purchases) else "❌ Ошибка сохранения!")
            wait_for_enter()
            break
        
        if choice in ["1", "2", "4"]:
            wait_for_enter()

# ========== СМЕНА РАБОЧЕЙ ДИРЕКТОРИИ ==========

@error_handler
@log_action
def change_directory() -> None:
    """Смена рабочей директории"""
    global working_directory
    
    clear_screen()
    print_header("СМЕНА РАБОЧЕЙ ДИРЕКТОРИИ")
    print(f"Текущая директория: {working_directory}")
    print("\nПодсказки:")
    
    hints = [
        "  • Абсолютный путь: C:/Users/User/Documents или /home/user/Documents",
        "  • Относительный путь: user/my/ или .. (родительская папка)",
        "  • '.' - текущая папка"
    ]
    print('\n'.join(hints))
    print("-" * 60)
    
    new_path = input("Введите новый путь: ").strip()
    
    if not new_path:
        print("❌ Путь не может быть пустым!")
        wait_for_enter()
        return
    
    # Тернарный оператор для определения пути
    target_path = os.path.normpath(
        new_path if os.path.isabs(new_path) else os.path.join(working_directory, new_path)
    )
    
    # Проверка с использованием тернарного оператора
    if os.path.exists(target_path) and os.path.isdir(target_path):
        working_directory = target_path
        print(f"✅ Рабочая директория изменена на:\n{working_directory}")
    else:
        print("❌ Путь не существует или не является папкой!")
    
    wait_for_enter()

# ========== ТЕСТЫ ==========

def run_tests() -> None:
    """Запуск тестов для новых функций"""
    print_header("ЗАПУСК ТЕСТОВ")
    
    tests_passed = 0
    tests_failed = 0
    
    # Тест 1: Проверка декоратора error_handler
    try:
        @error_handler
        def test_error_func():
            raise ValueError("Тестовая ошибка")
        
        test_error_func()
        print("✅ Тест 1 пройден: error_handler работает")
        tests_passed += 1
    except:
        print("❌ Тест 1 не пройден: error_handler")
        tests_failed += 1
    
    # Тест 2: Проверка генератора get_directory_items
    try:
        files, dirs = get_directory_items()
        assert isinstance(files, list) and isinstance(dirs, list)
        print("✅ Тест 2 пройден: get_directory_items работает")
        tests_passed += 1
    except:
        print("❌ Тест 2 не пройден: get_directory_items")
        tests_failed += 1
    
    # Тест 3: Проверка тернарных операторов
    try:
        test_value = 5
        result = "positive" if test_value > 0 else "negative"
        assert result == "positive"
        print("✅ Тест 3 пройден: тернарные операторы")
        tests_passed += 1
    except:
        print("❌ Тест 3 не пройден: тернарные операторы")
        tests_failed += 1
    
    # Тест 4: Проверка генераторов
    try:
        test_list = [1, 2, 3, 4, 5]
        gen = (x * 2 for x in test_list if x % 2 == 0)
        result = list(gen)
        assert result == [4, 8]
        print("✅ Тест 4 пройден: генераторы")
        tests_passed += 1
    except:
        print("❌ Тест 4 не пройден: генераторы")
        tests_failed += 1
    
    print(f"\nРезультаты тестов: Пройдено: {tests_passed}, Не пройдено: {tests_failed}")
    wait_for_enter()

# ========== ГЛАВНАЯ ПРОГРАММА ==========

@error_handler
def main() -> None:
    """Главная функция программы"""
    global working_directory
    
    # Словарь для вызова функций вместо множественных if-elif
    menu_actions = {
        "1": create_folder,
        "2": delete_item,
        "3": copy_item,
        "4": list_contents,
        "5": list_folders,
        "6": list_files,
        "7": system_info,
        "8": show_creator,
        "9": play_quiz,
        "10": bank_account,
        "11": change_directory,
        "12": save_directory_contents,
        "test": run_tests  # Скрытая команда для тестов
    }
    
    while True:
        choice = show_menu()
        
        if choice == "13":
            clear_screen()
            print("Спасибо за использование программы! До свидания!")
            sys.exit(0)
        elif choice in menu_actions:
            menu_actions[choice]()
        else:
            print("❌ Неверный пункт меню! Пожалуйста, выберите 1-13.")
            wait_for_enter()

if __name__ == "__main__":
    main()