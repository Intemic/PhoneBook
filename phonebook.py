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
    MAX_RECORD_IN_PAGE = 5
    FILE_NAME = 'book.txt'
    HEADER = '{:20} {:20} {:20} {:20} {:20} {:20}'.format(
        'Фамилия ',
        'Имя',
        'Отчество',
        'Организация',
        'Рабочий телефон',
        'Сотовый телефон'
    )
    SEARCH_MENU = {
        1: 'family',
        2: 'name',
        3: 'surname',
        4: 'organization',
        5: 'working_phone',
        6: 'mobile_phone'
    }
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
        while records:
            page += 1
            print(f'\nСтраница {page}')
            print(PhoneBook.HEADER)
            for record in records[:PhoneBook.MAX_RECORD_IN_PAGE]:
                print(record.get_message())
            records = records[PhoneBook.MAX_RECORD_IN_PAGE:]         

    @staticmethod
    def get_non_empty_value(text: str, value: str) -> str:
        '''Получение не пустого значения, имитация "обязательного" поля.'''
        while not value:
            value = input(text).strip()
        return value

    @staticmethod
    def get_correct_phone_number(text: str, value: str) -> str:
        # while not value:
        #     value = input(text).strip()
        #     # if not re.fullmatch('^((\+7|7|8)+([0-9]){10})$', value):
        #     if not re.fullmatch('^(8+([0-9]){10})$', value):
        #         value = ''

        return value

    def __init__(self) -> None:
        self.operations = {
            1: self.printing_telephone_directory,
            2: self.add_new_record,
            3: self.change_records,
            4: self.search_records,
        }

    def printing_telephone_directory(self):
        '''Вывод телефонного справочника.'''
        records = PhoneBook.get_records()
        if not records:
            print('Нет данных')
        else:
            PhoneBook.output_records(records)

    def add_new_record(self):
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

    def change_records(self):
        '''Изменить записи.'''
        pass

    def search_records(self):
        '''Поиск записей по параметрам'''
        records = PhoneBook.get_records()
        if not records:
            print('Нет данных, нечего искать')      
        else:
            print('\nВыберитье критерии поиска:', '\n')
            for key, item in PhoneBook.SEARCH_MENU.items():
                print(key, '-', PhoneBook.SEARCH_MENU_TEXT[item])
            print('Можно выбрать несколько пунктов, через пробел')

            while True:
                try:
                    inpt = input('Выберите пункт(ы) меню: ').strip()
                    if not inpt:
                        break
                        
                    #  сформируем перечень пунктов для заполнения   
                    #  вынесем отднльно чтобы проверить корректность ввода 
                    dict_search = {}
                    for item in map(int, inpt.split()):
                        dict_search[PhoneBook.SEARCH_MENU[item]] = None

                    for item in dict_search:
                        dict_search[item] = input(
                            f'Введите {PhoneBook.SEARCH_MENU_TEXT[item]}: '
                        )    

                    result = []
                    shablon = Record(**dict_search)
                    for rec in records:
                        if rec == shablon:
                            result.append(rec)
                    
                    print(f'\nНайдено {len(result)} соответствий:')
                    if len(result):
                        PhoneBook.output_records(result)
                    break
                        
                except (ValueError, KeyError):
                    print('Выберите действительное значение', )

    def show_menu(self):
        '''Вывод меню и вызов обработчика для пункта меню.'''

        while True:
            print('\nТелефонный справочник, возможные операции:', '\n')
            print('0 - Выход из программы')
            print('1 - Вывод содержимого')
            print('2 - Добавление новой записи')
            print('3 - Изменить запись')
            print('4 - Поиск записи\n')

            try:
                result = int(input('Выберите пункт меню: ').strip())
                if not result:
                    self.fobj.close()
                    break

                self.operations[result]()
            except ValueError:
                print('Выберите действительное значение', )
            except Exception:
                print('Что то пошло нет так: ')
                break


if __name__ == '__main__':
    phone_book = PhoneBook()
    rec = Record(name='Anton', family='Luchik')
    #print(asdict(rec))
    phone_book.add_new_record()
    #phone_book.printing_telephone_directory()
    # phone_book.search_records()
