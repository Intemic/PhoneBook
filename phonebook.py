import pickle
import csv
import re
from dataclasses import dataclass, asdict

@dataclass
class Record:
    '''Представляет запись о человеке в телефонной книге.'''

    PRINT_TEMPLATE = (
        '{family:20} {name:20} {surname:20}'
        '{working_phone:^20}'
        '{mobile_phone:^20}'
    )

    family: str
    name: str
    surname: str
    organization: str
    working_phone: str
    mobile_phone: str

    def get_message(self) -> str:
        '''Вывод записи.'''
        return self.PRINT_TEMPLATE.format(**asdict(self))


class PhoneBook:
    MAX_RECORD_IN_PAGE = 5
    FILE_NAME = 'book.txt'
    HEADER = '{:20} {:20} {:20} {:20} {:20}'.format(
        'Фамилия ',
        'Имя',
        'Отчество',
        'Рабочий телефон', 
        'Сотовый телефон'
    )

    def __init__(self, file_name: str = 'book.txt') -> None:
        # self.records = []

        self.operations = {
            1: self.printing_telephone_directory,
            2: self.add_new_record,
            3: self.change_records,
            4: self.search_records,
        }

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

    def printing_telephone_directory(self):
        '''Вывод телефонного справочника.'''
        with open(PhoneBook.FILE_NAME, encoding='utf-8') as f:
            records = [Record(**record) for record in csv.DictReader(f,  delimiter=';')]

        if not records:
            print('Нет данных')
        else:    
            page = 0
            while records:
                page += 1
                print(f'\nСтраница {page}')
                print(PhoneBook.HEADER)
                for record in records[:PhoneBook.MAX_RECORD_IN_PAGE]:
                    print(record.get_message())
                    print(asdict(record))
                records = records[PhoneBook.MAX_RECORD_IN_PAGE:]

    def add_new_record(self):
        '''Добавление новой записи.'''
        print('Введите следующие данные:')
        family, name, surname, organization, working_phone, mobile_phone = '', '', '', '', '', '' 
        family = PhoneBook.get_non_empty_value('Фамилия:', family)
        name = ''
        name = PhoneBook.get_non_empty_value('Имя:', name) 
        surname = ''
        surname = PhoneBook.get_non_empty_value('Отчество:', surname)
        organization = input('Организация:')
        working_phone = PhoneBook.get_correct_phone_number('Рабочий телефон:', working_phone)
        mobile_phone = PhoneBook.get_correct_phone_number('Сотовый телефон:', mobile_phone)

        rec = list(asdict(
                Record(
                    family,
                    name,
                    surname,
                    organization,
                    working_phone,
                    mobile_phone
                )
            )
        )

        with open(PhoneBook.FILE_NAME, encoding='utf-8', mode='a+') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=list(rec.keys()), quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(**rec)

    def change_records(self):
        '''Изменить записи.'''
        pass    

    def search_records(self):
        '''Поиск записей по параметрам'''
        pass   

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
            except Exception as ex:    
                print('Что то пошло нет так: ')
                break


if __name__ == '__main__':
    phone_book = PhoneBook()
    phone_book.show_menu()
