import json
import os

# Имя файла для хранения контактов
FILENAME = 'contacts.json'

# Глобальный словарь для хранения контактов (ключ - ID, значение - словарь с данными)
contacts = {}
next_id = 1
changed = False

def load_contacts():
    global contacts, next_id
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as file:
            data = json.load(file)
            contacts = {int(k): v for k, v in data.items()}
            if contacts:
                next_id = max(contacts.keys()) + 1
            else:
                next_id = 1
    else:
        contacts = {}
        next_id = 1
    print("Контакты успешно загружены.")

def save_contacts():
    global changed
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump({str(k): v for k, v in contacts.items()}, file, ensure_ascii=False, indent=4)
    changed = False
    print("Контакты сохранены в файл.")

def show_contacts():
    if not contacts:
        print("Нет контактов.")
        return
    print(f"{'ID':<5} {'Имя':<20} {'Телефон':<15} {'Комментарий'}")
    for cid, contact in contacts.items():
        print(f"{cid:<5} {contact['name']:<20} {contact['phone']:<15} {contact['comment']}")

def create_contact():
    global next_id, changed
    name = input("Введите имя: ").strip()
    phone = input("Введите телефон: ").strip()
    comment = input("Комментарий (можно оставить пустым): ").strip()
    contacts[next_id] = {'name': name, 'phone': phone, 'comment': comment}
    print(f"Контакт добавлен с ID {next_id}.")
    next_id += 1
    changed = True

def find_contacts():
    keyword = input("Введите поисковое слово: ").strip().lower()
    results = []
    for cid, contact in contacts.items():
        if (keyword in contact['name'].lower() or
            keyword in contact['phone'].lower() or
            keyword in contact['comment'].lower()):
            results.append((cid, contact))
    if results:
        print(f"{'ID':<5} {'Имя':<20} {'Телефон':<15} {'Комментарий'}")
        for cid, contact in results:
            print(f"{cid:<5} {contact['name']:<20} {contact['phone']:<15} {contact['comment']}")
    else:
        print("Контакты не найдены.")

def edit_contact():
    global changed
    try:
        cid = int(input("Введите ID контакта для редактирования: "))
        if cid in contacts:
            print(f"Текущие данные: {contacts[cid]}")
            name = input("Новое имя (оставьте пустым, чтобы оставить текущим): ").strip()
            phone = input("Новый телефон (оставьте пустым): ").strip()
            comment = input("Новый комментарий (оставьте пустым): ").strip()
            if name:
                contacts[cid]['name'] = name
            if phone:
                contacts[cid]['phone'] = phone
            if comment:
                contacts[cid]['comment'] = comment
            print("Контакт обновлён.")
            changed = True
        else:
            print("Контакт с таким ID не найден.")
    except ValueError:
        print("Некорректный ввод.")

def delete_contact():
    global changed
    try:
        cid = int(input("Введите ID контакта для удаления: "))
        if cid in contacts:
            del contacts[cid]
            print("Контакт удалён.")
            changed = True
        else:
            print("Контакт с таким ID не найден.")
    except ValueError:
        print("Некорректный ввод.")

def main():
    load_contacts()
    while True:
        print("\nМеню:")
        print("1. Открыть файл")
        print("2. Сохранить файл")
        print("3. Показать все контакты")
        print("4. Создать контакт")
        print("5. Найти контакт")
        print("6. Изменить контакт")
        print("7. Удалить контакт")
        print("8. Выход")
        choice = input("Выберите действие (1-8): ").strip()

        if choice == '1':
            load_contacts()
        elif choice == '2':
            save_contacts()
        elif choice == '3':
            show_contacts()
        elif choice == '4':
            create_contact()
        elif choice == '5':
            find_contacts()
        elif choice == '6':
            edit_contact()
        elif choice == '7':
            delete_contact()
        elif choice == '8':
            if changed:
                save_prompt = input("Есть несохранённые изменения. Сохранить? (y/n): ").strip().lower()
                if save_prompt == 'y':
                    save_contacts()
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()