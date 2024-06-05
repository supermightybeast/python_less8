from csv import DictReader, DictWriter
from os.path import exists

class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

class LenNameError(Exception):
    def __init__(self, txt):
        self.txt = txt

print('Список команд для пользования справочником: ')
print('- q - выйти из справочника.')
print('- w - создать новый контакт и записать его в файл.')
print('- r - прочитать все контакты из файла и вывести их на экран.')
print('- copy - скопировать один контакт из файла в другой файл.')
print('- c - изменить или удалить контакт.')

def get_info():
    first_name = input('Введите имя: ')
    last_name = input('Введите фамилию: ')
    is_valid_name = False
    while not is_valid_name:
        try:
            if len(first_name) < 2 or len(last_name) < 2:
                raise LenNameError('Некорректная длина имени или фамилии')
            else:
                is_valid_name = True
        except LenNameError as err:
            print(err)
            first_name = input('Введите имя: ')
            last_name = input('Введите фамилию: ')

    is_valid_number = False
    while not is_valid_number:
        try: 
            phone_number = int(input('Введите 11-значный номер тефелона: '))
            if len(str(phone_number)) != 3:
                raise LenNumberError('Некорректная длина номера')
            else:
                is_valid_number = True
        except ValueError:
            print('Некорректный номер')
        except LenNumberError as err:
            print(err)
    return {'имя': first_name, 'фамилия': last_name, 'телефон': phone_number}

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['имя', 'фамилия', 'телефон'])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def write_file(file_name, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as file:
        f_writer = DictWriter(file, fieldnames=['имя', 'фамилия', 'телефон'])
        if file.tell() == 0:
            f_writer.writeheader()
        f_writer.writerow(data)

def update_data(file_name):
    data = read_file(file_name)
    updated_data = []
    search_key = input('Введите имя или фамилию для поиска: ')
    for row in data:
        if row['имя'] == search_key or row['фамилия'] == search_key:
            new_value = input(f'Введите новое значение для поля {row["имя"]}: ')
            row['имя'] = new_value
        updated_data.append(row)
    write_file(file_name, updated_data)
    print('Данные успешно обновлены')

def delete_data(file_name):
    data = read_file(file_name)
    updated_data = []
    search_key = input('Введите имя или фамилию для поиска: ')
    for row in data:
        if row['имя'] != search_key and row['фамилия'] != search_key:
            updated_data.append(row)
    write_file(file_name, updated_data)
    print('Данные успешно удалены')

import csv

def copy_data(file_name, destination_file):
    data = read_file(file_name)
    copied_data = []
    row_number = int(input('Введите номер строки, которую необходимо скопировать: '))
    if row_number < 1 or row_number > len(data):
        print('Некорректный номер строки')
        return
    copied_data = data[row_number - 1]
    write_file(destination_file, copied_data)
    print('Данные успешно скопированы')

file_name = 'phone.csv'

def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            data = get_info()
            write_file(file_name, data)
        elif command == 'r':
            if not exists(file_name):
                print('Файл не создан. Создайте его.')
                continue
            print(*read_file(file_name))
        elif command == 'copy':
            destination_file = input('Введите имя файла, в который нужно скопировать данные: ')
            copy_data(file_name, destination_file)
            continue
        elif command == 'c':
            action = input('Введите действие (изменить или удалить): ')
            if action == 'изменить':
                update_data(file_name)
            elif action == 'удалить':
                delete_data(file_name)
            else:
                print('Неверное действие')
        else:
            print('Неверная команда')

main()