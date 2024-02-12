import pickle
from dataclasses import dataclass, asdict

@dataclass
class Record:
    '''Представляет запись о человеке в телефонной книге.'''

    PRINT_TEMPLATE = (
        'Фамилия:         {family}\n'
        'Имя:             {name}\n'
        'Отчество:        {surname}\n'
        'Рабочий телефон: {working_phone}\n'
        'Сотовый телефон: {mobile_phone}'
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
    def __init__(self, file_name: str = 'book.txt') -> None:
        self.records = []

        self.operations = {
            1: self.printing_telephone_directory,
            2: self.add_new_record,
            3: self.change_records,
            4: self.search_records,
        }

        self.fobj = open(file_name, 'ab+')

    @staticmethod
    def get_non_empty_value(text: str, value: str) -> str:
        '''Получение не пустого значения, имитация "обязательного" поля.'''
        while not value:
            value = input(text).strip()
        return value

    @staticmethod
    def get_correct_phone_number(text: str, value: str) -> str:
        return value

    def printing_telephone_directory(self):
        '''Вывод телефонного справочника.'''
        for record in self.records:
            print(record.get_message())

    def add_new_record(self):
        '''Добавление новой записи.'''
        print('Введите следующие данные:')
        family, name, surname, organization, working_phone, mobile_phone = '', '', '', '', '', '' 
        family = PhoneBook.get_non_empty_value('Фамилия:', family)
        name = ''
        name = PhoneBook.get_non_empty_value('Имя:', name) 
        surname = ''
        surname = PhoneBook.get_non_empty_value('Отчество:', surname)
        # organization = input('Организация:')
        working_phone = PhoneBook.get_correct_phone_number('Рабочий телефон:', working_phone)
        mobile_phone = PhoneBook.get_correct_phone_number('Сотовый телефон:', mobile_phone)

        self.records.append(Record(
                family,
                name,
                surname,
                organization,
                working_phone,
                mobile_phone
            )
        )
        
        pickle.dump(
            self.records[-1],
            self.fobj
        )

        print('Создана запись: ', (self.records[-1]).get_message())


    def change_records(self):
        '''Изменить записи.'''
        pass    

    def search_records(self):
        '''Поиск записей по параметрам'''
        pass   

    def show_menu(self):
        '''Вывод меню и вызов обработчика для пункта меню.'''

        while True:
            print('Телефонный справочник, возможные операции:', '\n')
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
