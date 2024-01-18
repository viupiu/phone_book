import os

# функция для ввода данных
def input_data():
    input_phone = input('Введите телефон: ') or "--"
    input_last_name = input('Введите фамилию: ') or "--"
    input_first_name = input('Введите имя: ') or "--"
    input_middle_name = input('Введите отчество: ') or "--"

    with open('phone.txt', 'a') as file:
        file.write(f"{input_phone}\t{input_last_name}\t{input_first_name}\t{input_middle_name}\n")

    print(f'\nСохранен контакт: {input_last_name} {input_first_name} {input_middle_name}\n')


# функция для вывода данных
def print_data():
    with open('phone.txt', 'r') as file:
        lines = file.readlines()

    if lines:
        print('Ваши контакты:\n')
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")
    else:
        print('Справочник пуст.')
    print('\n')


# функция для поиска данных
def search_data():
    input_data = input('Введите запрос: ').lower()
    found_contacts = []

    with open('phone.txt', 'r') as file:
        for line in file:
            if input_data in line.lower():
                found_contacts.append(line.strip())

    if found_contacts:
        if len(found_contacts) == 1:
            print(f"Найден контакт: {found_contacts[0]}\n")
            edit_data(found_contacts)
        else:
            print(f"Найдено контактов: {len(found_contacts)}")
            for i, contact in enumerate(found_contacts, start=1):
                print(f"{i}. {contact}")
            edit_data(found_contacts)
            print('\n')
    else:
        print("Контакт не найден\n")


# функция для поиска данных для удаления
def delete_data():
    input_data = input('Что нужно удалить (или "ВСЕ" для удаления всех контактов): ').lower()

    found_contacts = []

    with open('phone.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if input_data in line.lower():
                found_contacts.append(line.strip())

    if input_data == 'все':
        user_confirm = input("Вы уверены, что хотите удалить все контакты? (Д/Н) \n").lower()
        if user_confirm == 'д':
            delete_all_contacts()
            print("Все контакты успешно удалены.\n")
            print_data()
        elif user_confirm == 'н':
            print("Удаление отменено.\n")
        else:
            print("Неверный ввод. Действие отменено.\n")

    elif found_contacts:
        if len(found_contacts) == 1:
            print(f"Найден контакт:")
            print(found_contacts[0])
            user_input = input("У - удалить контакт\nВ - выход из меню\n").lower()
            if user_input == 'у':
                delete_single_contact(found_contacts[0], lines)
                print_data()
            elif user_input == 'в':
                print("Выход из меню.\n")
            else:
                print("Неверный ввод. Действие отменено.\n")
        elif len(found_contacts) > 1:
            print(f"Найдено контактов: {len(found_contacts)}")
            for i, contact in enumerate(found_contacts, start=1):
                print(f"{i}. {contact}")

            user_input = input("Выберите номер контакта для удаления\nВСЕ - удалить все\nВ - выход из меню\n").lower()

            if user_input.isdigit() and 1 <= int(user_input) <= len(found_contacts):
                selected_contact = found_contacts[int(user_input) - 1]
                delete_single_contact(selected_contact, lines)
                print(f"Успешно удален контакт: {selected_contact}")
            elif user_input == 'в':
                print("Выход из меню.\n")
            else:
                print("Неверный ввод. Действие отменено.\n")
    else:
        print("Контакт не найден\n")


# функция для удаления контакта
def delete_single_contact(selected_contact, lines):
    with open('phone.txt', 'w') as file:
        for line in lines:
            if selected_contact.lower() not in line.lower():
                file.write(line)
    print(f"Успешно удален контакт: {selected_contact}\n")


# функция для удаления всех контактов
def delete_all_contacts():
    with open('phone.txt', 'w'):
        print("Все контакты успешно удалены.\n")


# функция для поиска контактов для изменения
def edit_data(found_contacts):
    if len(found_contacts) == 1:
        user_input = input("И - изменить контакт\nУ - удалить контакт\nВ - выход из меню\n").lower()
        if user_input == 'и':
            user_input = '1'
        elif user_input == 'у':
            delete_single_contact(found_contacts[0], lines)
            print_data()
            return
    else:
        user_input = input("\nВыберите номер контакта для изменения\nВ - выход из меню\n").lower()

    if user_input.isdigit() and 1 <= int(user_input) <= len(found_contacts):
        selected_contact = found_contacts[int(user_input) - 1]
        edit_or_delete(selected_contact)
    elif user_input == 'в':
        print("Выход из меню.\n")
    else:
        print("Неверный ввод. Действие отменено.\n")


# функция для выбора, что сделать с контактом - изменить или удалить
def edit_or_delete(selected_contact):
    with open('phone.txt', 'r') as file:
        lines = file.readlines()

        user_choice = input(
            f"\nВыбран контакт: {selected_contact}\nИ - изменить\nУ - удалить\nВ - выйти из меню\n").lower()

        if user_choice == 'и':
            edit_single_contact(selected_contact, lines)
        elif user_choice == 'у':
            delete_single_contact(selected_contact, lines)
            print_data()
        elif user_choice == 'в':
            print("Выход из меню.\n")
        else:
            print("Неверный ввод. Действие отменено.\n")


# функция для изменения контакта
def edit_single_contact(found_contact, lines):
    print(f"Редактирование контакта: {found_contact}\n")

    for i, line in enumerate(lines):
        if line.strip() == found_contact:
            parts = line.strip().split('\t')  # изменено на использование табуляции
            if len(parts) == 4:
                current_phone, current_last_name, current_first_name, current_middle_name = parts

                input_phone = input(
                    f'Текущий телефон: {current_phone}\nВведите новый телефон (оставьте пустым, чтобы оставить прежний): ') or current_phone
                input_last_name = input(
                    f'Текущая фамилия: {current_last_name}\nВведите новую фамилию (оставьте пустым, чтобы оставить прежнюю): ') or current_last_name
                input_first_name = input(
                    f'Текущее имя: {current_first_name}\nВведите новое имя (оставьте пустым, чтобы оставить прежнее): ') or current_first_name
                input_middle_name = input(
                    f'Текущее отчество: {current_middle_name}\nВведите новое отчество (оставьте пустым, чтобы оставить прежнее): ') or current_middle_name

                updated_contact = f"{input_phone}\t{input_last_name}\t{input_first_name}\t{input_middle_name}\n"  # изменено на использование табуляции
                lines[i] = updated_contact

                with open('phone.txt', 'w') as file:
                    file.writelines(lines)

                print(f'\nУспешно обновлен контакт: {input_last_name} {input_first_name} {input_middle_name}\n')
                return

    print("Контакт не найден.\n")


# основная функция
def main():
    while True:
        with open('phone.txt', 'r') as file:
            lines = file.readlines()

        if not lines:
            data_input = input('Д - Добавить контакт\n'
                               'В - Выход\n').lower()
        else:
            data_input = input('Д - Добавить контакт\n'
                               'С - Список контактов\n'
                               'П - Поиск\n'
                               'У - Удалить контакт\n'
                               'В - Выход\n').lower()

        if data_input not in {'д', 'с', 'п', 'у', 'в'}:
            print('Ошибка ввода.')
        else:
            if data_input == 'д':
                input_data()
            elif data_input == 'с':
                print_data()
            elif data_input == 'п':
                search_data()
            elif data_input == 'у':
                delete_data()
            else:
                print('До свидания!')
                break


print('Добро пожаловать в телефонную книгу!')
if __name__ == "__main__":
    main()