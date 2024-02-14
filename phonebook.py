import csv
import re
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
    SEARCH_MENU_KEY = {
        1: 'family',
        2: 'name',
        3: 'surname',
        4: 'organization',
        5: 'working_phone',
        6: 'mobile_phone'
    }
    # текстовка к меню поиска
    SEARCH_MENU_TEXT = {
        'family': 'Фамилия',
        'name': 'Имя',
        'surname': 'Отчество',
        'organization': 'Организация',
        'working_phone': 'Рабочий телефон',
        'mobile_phone': 'Сотовый телефон'
    }

    @staticmethod
    def get_records() -> list[Record]:
        records = []
        try:
            with open(PhoneBook.FILE_NAME, encoding='utf-8') as f:
                records = [
                    Record(**record) for record in csv.DictReader(
                        f,  delimiter=';'
                    )
                ]
        except Exception:
            # не удалось открыть файл, значит нет данных
            pass

        return records

    def output_records(records: list[Record]) -> None:
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
        while not value:
            value = input(text).strip()
            if not re.fullmatch('^(8+([0-9]){10})$', value):
                value = ''

        return value

    @staticmethod
    def get_select_items_menu(menu: dict) -> list[int]:
        sel = []
        while True:
            try:
                inpt = input('Выберите пункт(ы) меню: ').strip()
                if not inpt:
                    continue

                #  сформируем перечень пунктов для заполнения
                #  вынесем отдельно чтобы проверить корректность ввода
                for item in map(int, inpt.split()):
                    dict_search[PhoneBook.SEARCH_MENU_KEY[item]] = None

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

        print('Введите следующие данные:')
        family, name, surname, organization, = '', '', '', ''
        working_phone, mobile_phone = '', ''
        family = PhoneBook.get_non_empty_value('Фамилия:', family)
        name = ''
        name = PhoneBook.get_non_empty_value('Имя:', name)
        surname = ''
        # surname = PhoneBook.get_non_empty_value('Отчество:', surname)
        # organization = input('Организация:')
        # working_phone = PhoneBook.get_correct_phone_number(
        #     'Рабочий телефон:', working_phone
        # )
        # mobile_phone = PhoneBook.get_correct_phone_number(
        #     'Сотовый телефон:', mobile_phone
        # )

        # rec = []
        # rec.append(asdict(
        #         Record(
        #             family,
        #             name,
        #             surname,
        #             organization,
        #             working_phone,
        #             mobile_phone
        #         )
        #     )
        # )

        # with open(PhoneBook.FILE_NAME, encoding='utf-8', mode='a+') as f:
        #     writer = csv.DictWriter(
        #         f,
        #         fieldnames=list(rec[0].keys()),
        #         quoting=csv.QUOTE_NONE,
        #         delimiter=';',
        #         dialect=csv.unix_dialect
        #     )
        #     writer.writerow(rec[0])
        print('1', '2', sep=';', file=open(PhoneBook.FILE_NAME, encoding='utf-8', mode='a+'))

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
            try:
                rec = records[
                    int(input('\nВыберите номер записи для изменения: ').strip())
                ]

                # выведем запись для просмотра
                print('Изменяемая запись:')
                print(rec.get_message())

            except ValueError:
                print('Выберите действительное значение', )
            except IndexError:
                print('Выберите действительный номер записи', )
            except Exception:
                print('Что то пошло нет так: ')
                break


    @staticmethod
    def search_records():
        '''Поиск записей по параметрам.'''

        records = PhoneBook.get_records()
        if not records:
            print('Нет данных, нечего искать')
        else:
            print('\nВыберите критерии поиска:', '\n')
            for key, item in PhoneBook.SEARCH_MENU_KEY.items():
                print(key, '-', PhoneBook.SEARCH_MENU_TEXT[item])
            print('Можно выбрать несколько пунктов, через пробел')

            while True:
                try:
                    inpt = input('Выберите пункт(ы) меню: ').strip()
                    if not inpt:
                        break

                    #  сформируем перечень пунктов для заполнения
                    #  вынесем отдельно чтобы проверить корректность ввода
                    dict_search = {}
                    for item in map(int, inpt.split()):
                        dict_search[PhoneBook.SEARCH_MENU_KEY[item]] = None

                    for item in dict_search:
                        dict_search[item] = input(
                            f'Введите {PhoneBook.SEARCH_MENU_TEXT[item]}: '
                        )

                    result = []
                    shablon = Record(**dict_search)
                    result = [rec for rec in records if rec == shablon]

                    print(f'\nНайдено {len(result)} соответствий:')
                    if len(result):
                        PhoneBook.output_records(result)
                    break

                except (ValueError, KeyError):
                    print('Выберите действительное значение', )

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
    rec = Record(name='Anton', family='Luchik')
    #print(asdict(rec))
    #phone_book.add_new_record()
    #phone_book.printing_telephone_directory()
    # phone_book.search_records()
    phone_book.change_records()
