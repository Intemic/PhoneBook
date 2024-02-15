import csv
import re
import os.path
from dataclasses import dataclass, asdict


@dataclass
class Record:
    '''Представляет запись о человеке в телефонной книге.'''

    PRINT_TEMPLATE = (
        '{family:20} {name:20} {surname:20} {organization:20}'
        '{working_phone:^20}'
        '{mobile_phone:^20}'
    )

    family: str = None
    name: str = None
    surname: str = None
    organization: str = None
    working_phone: str = None
    mobile_phone: str = None

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Record):
            return False

        result = True

        if (self.family is not None and
           obj.family is not None):
            result = bool(
                result and
                self.family.lower() == obj.family.lower()
            )

        if (self.name is not None and
           obj.name is not None):
            result = bool(
                result and self.name.lower() == obj.name.lower()
            )

        if (self.surname is not None and
           obj.surname is not None):
            result = bool(
                result and self.surname.lower() == obj.surname.lower()
            )

        if (self.organization is not None and
           obj.organization is not None):
            result = bool(
                result and
                self.organization.lower() == obj.organization.lower()
            )

        if (self.working_phone is not None and
           obj.working_phone is not None):
            result = bool(
                result and
                self.working_phone.lower() == obj.working_phone.lower()
            )

        if (self.mobile_phone is not None and
           obj.mobile_phone is not None):
            result = bool(
                result and
                self.mobile_phone.lower() == obj.mobile_phone.lower()
            )

        return result

    def get_message(self) -> str:
        '''Вывод записи.'''
        return self.PRINT_TEMPLATE.format(**asdict(self))


class PhoneBook:
    # кол-во записей на странице
    MAX_RECORD_IN_PAGE = 5
    # имя файла с данными
    FILE_NAME = 'book.txt'
    # заголовок таблицы
    HEADER = '{:5} {:20} {:20} {:20} {:20} {:20} {:20}'.format(
        '№',
        'Фамилия ',
        'Имя',
        'Отчество',
        'Организация',
        'Рабочий телефон',
        'Сотовый телефон'
    )
    # основное меню
    MAIN_MENU = {
        0: ('Выход из программы', None),
        1: ('Вывод содержимого', 'printing_telephone_directory'),
        2: ('Добавление новой записи', 'add_new_record'),
        3: ('Изменить запись', 'change_records'),
        4: ('Поиск записи', 'search_records')
    }
    # меню поиска
    RECORD_MENU_KEY = {
        1: 'family',
        2: 'name',
        3: 'surname',
        4: 'organization',
        5: 'working_phone',
        6: 'mobile_phone'
    }
    # текстовка к меню поиска
    RECORD_MENU_TEXT = {
        'family': 'Фамилия',
        'name': 'Имя',
        'surname': 'Отчество',
        'organization': 'Организация',
        'working_phone': 'Рабочий телефон',
        'mobile_phone': 'Сотовый телефон'
    }

    @staticmethod
    def get_records() -> list[Record]:
        '''Возращает перечень записей телефоной книги.'''

        records = []
        try:
            with open(PhoneBook.FILE_NAME, encoding='utf-8') as f:
                records = [
                    Record(**record) for record in csv.DictReader(
                        f,  delimiter=';'
                    )
                ]
        except Exception:
            # не удалось открыть файл, справочник пуст
            pass

        return records

    def output_records(records: list[Record]) -> None:
        '''Отображает список записей тел. книги.'''

        page = 0
        indx = 0
        while records:
            page += 1
            print(f'\nСтраница {page}')
            print(PhoneBook.HEADER)
            for record in records[:PhoneBook.MAX_RECORD_IN_PAGE]:
                indx += 1
                print(f'{indx:<5}', record.get_message())
            records = records[PhoneBook.MAX_RECORD_IN_PAGE:]

    @staticmethod
    def get_non_empty_value(text: str, value: str) -> str:
        '''Получение не пустого значения, имитация "обязательного" поля.'''

        while not value:
            value = input(text).strip()
        return value

    @staticmethod
    def get_correct_phone_number(text: str, value: str) -> str:
        '''Проверка ввода телефоного номера на корректность.'''

        while not value:
            value = input(text).strip()
            if not re.fullmatch('^(8+([0-9]){10})$', value):
                print('Некорректное значение')
                value = ''

        return value

    @staticmethod
    def get_select_items_menu(menu: dict, text: str, convert: bool = True) -> list[int]:
        while True:
            sel = []
            try:
                inpt = input(text).strip()
                if not inpt:
                    continue

                for item in inpt.split():
                    if convert:
                        item = int(item)

                    if item in menu:
                        sel.append(item)
                    else:
                        raise KeyError('Некорректный ключ')

                return sel

            except (ValueError, KeyError):
                print('Выберите действительное значение', )

    @staticmethod
    def printing_telephone_directory():
        '''Вывод телефонного справочника.'''
        records = PhoneBook.get_records()
        if not records:
            print('Нет данных')
        else:
            PhoneBook.output_records(records)

    @staticmethod
    def add_new_record():
        '''Добавление новой записи.'''

        while True:
            print('\nВведите следующие данные:')
            family, name, surname, organization, = '', '', '', ''
            working_phone, mobile_phone = '', ''
            family = PhoneBook.get_non_empty_value('Фамилия:', family)
            name = PhoneBook.get_non_empty_value('Имя:', name)
            surname = PhoneBook.get_non_empty_value('Отчество:', surname)
            organization = input('Организация:')
            working_phone = PhoneBook.get_correct_phone_number(
                'Рабочий телефон:', working_phone
            )
            mobile_phone = PhoneBook.get_correct_phone_number(
                'Сотовый телефон:', mobile_phone
            )

            obj = Record(
                family,
                name,
                surname,
                organization,
                working_phone,
                mobile_phone
            )

            file_exist = os.path.exists(PhoneBook.FILE_NAME)

            with open(PhoneBook.FILE_NAME, encoding='utf-8', mode='a+') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=list(obj.__dict__.keys()),
                    quoting=csv.QUOTE_NONE,
                    delimiter=';',
                    dialect=csv.unix_dialect
                )
                if not file_exist:
                    writer.writeheader()
                writer.writerow(asdict(obj))

            sel = PhoneBook.get_select_items_menu(
                {'y': None, 'n': None},
                '\nВвести еще одну запись(y/n)?: ',
                convert=False
            )

            if sel[0] == 'n':
                break           

    @staticmethod
    def change_records():
        '''Изменить записи.'''

        # выведем все записи, для выбора
        records = PhoneBook.get_records()
        if not records:
            print('Отсутствуют записи для изменения')
            return

        PhoneBook.output_records(records)

        while True:
            # получим выбор пользователя    
            sel = PhoneBook.get_select_items_menu(
                {i + 1: None for i in range(len(records))},
                '\nВыберите номер записи для изменения: '
            )

            obj = records[sel[0] - 1]
            # выберем что меняем 
            print('\nВыберите аттрибуты для изменения:', '\n')
            for key, item in PhoneBook.RECORD_MENU_KEY.items():
                print(key, '-', PhoneBook.RECORD_MENU_TEXT[item])
            print('Можно выбрать несколько пунктов, через пробел')

            sel_items = PhoneBook.get_select_items_menu(
                PhoneBook.RECORD_MENU_KEY,
                '\nВыберите пункт(ы) меню: '
            )

            for item in sel_items:
                obj.__dict__[PhoneBook.RECORD_MENU_KEY[item]] = input(
                    f'Введите {
                        PhoneBook.RECORD_MENU_TEXT[
                            PhoneBook.RECORD_MENU_KEY[item]
                        ]
                    }: '
                )
        
            sel = PhoneBook.get_select_items_menu(
                {'y': None, 'n': None},
                '\nИзменить другую запись(y/n)?: ',
                convert=False
            )

            if sel[0] == 'n':
                break
        
        # сохраним изменения
        with open(PhoneBook.FILE_NAME, encoding='utf-8', mode='w') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=list(records[0].__dict__.keys()),
                quoting=csv.QUOTE_NONE,
                delimiter=';',
                dialect=csv.unix_dialect
            )
            writer.writeheader()
            for rec in records:
                writer.writerow(asdict(rec))       


    @staticmethod
    def search_records():
        '''Поиск записей по параметрам.'''

        records = PhoneBook.get_records()
        if not records:
            print('Нет данных, нечего искать')
        else:
            while True:
                print('\nВыберите критерии поиска:', '\n')
                for key, item in PhoneBook.RECORD_MENU_KEY.items():
                    print(key, '-', PhoneBook.RECORD_MENU_TEXT[item])
                print('Можно выбрать несколько пунктов, через пробел')

                sel_items = PhoneBook.get_select_items_menu(
                    PhoneBook.RECORD_MENU_KEY,
                    '\nВыберите пункт(ы) меню: '
                )

                #  сформируем перечень пунктов для заполнения
                dict_search = {}
                for item in sel_items:
                    dict_search[PhoneBook.RECORD_MENU_KEY[item]] = None

                for item in dict_search:
                    dict_search[item] = input(
                        f'Введите {PhoneBook.RECORD_MENU_TEXT[item]}: '
                    )

                result = []
                shablon = Record(**dict_search)
                # примитивный поиск, можно конечно и сложнее
                result = [rec for rec in records if rec == shablon]

                print(f'\nНайдено {len(result)} соответствий:')
                if len(result):
                    PhoneBook.output_records(result)
                
                sel = PhoneBook.get_select_items_menu(
                    {'y': None, 'n': None},
                    '\nХотите продолжить поиск(y/n)?: ',
                    convert=False
                )

                if sel[0] == 'n':
                    break

    @staticmethod
    def show_menu():
        '''Вывод меню и вызов обработчика для пункта меню.'''

        while True:
            print('\nТелефонный справочник, возможные операции:', '\n')
            for key, item in PhoneBook.MAIN_MENU.items():
                print(key, '-', item[0])
            print('')

            try:
                result = int(input('Выберите пункт меню: ').strip())
                if not result:
                    break

                getattr(globals()['PhoneBook'], PhoneBook.MAIN_MENU[result][1])()
            except ValueError:
                print('Выберите действительное значение', )
            except Exception:
                print('Что то пошло нет так: ')
                break


if __name__ == '__main__':
    phone_book = PhoneBook()
    phone_book.show_menu()
