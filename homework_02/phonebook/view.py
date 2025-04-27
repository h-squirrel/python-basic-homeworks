from enum import Enum

class PBVGetContactNumArgs(Enum):
    CHANGE_CONTACT     = 1
    DELETE_CONTACT     = 2
    SHOW_CONTACT_INFO  = 3

class PBVPrintInfoMsgArg(Enum):
    PB_NOT_OPEN       = 1
    EMPTY_PB_LIST     = 2
    EMPTY_FIND_LIST   = 3
    SC_OPEN_PB        = 4
    SC_ADD_CONTACT    = 5
    SC_SAVED_CHANGES  = 6
    SC_CHANGE_CONTACT = 7
    SC_DELETE_CONTACT = 8
    PB_CLOSE          = 9

class PhoneBookView:

    @staticmethod
    def get_contact_number(world_to_return: str, action: PBVGetContactNumArgs, contact_list_size: int) -> str:
        print(f"Чтобы вернуться в главное меню введите {world_to_return}")
        print(f"Количество записей в телефонной книге - {contact_list_size}")
        if PBVGetContactNumArgs.CHANGE_CONTACT == action:
            data = input(f"Введите номер записи для изменения данных контакта: ")
        elif PBVGetContactNumArgs.DELETE_CONTACT == action:
            data = input(f"Введите номер записи для удаления: ")
        elif PBVGetContactNumArgs.SHOW_CONTACT_INFO:
            data = input(f"Введите номер записи для просмотра подробной информации о контакте: ")
        else:
            data = input(f"Введите номер записи: ")
        return data

    @staticmethod
    def get_data_for_find(world_to_return: str) -> str:
        print(f"Чтобы вернуться в главное меню введите {world_to_return}")
        data = input("Введите данные для поиска контактов:")
        return data

    @staticmethod
    def get_field_name(world_to_return: str) -> str:
        print(f"Чтобы вернуться в главное меню введите {world_to_return}")
        field_name = input("Какое поле записи вы хотите изменить? (phone, name, lastname, birthday, note): ")
        return field_name

    @staticmethod
    def get_field_value(world_to_return: str, field_name: str, field_desc: str) -> str:
        print(f"Чтобы вернуться в главное меню введите {world_to_return}")
        if "" == field_desc:
            print(f"Введите значение поля {field_name}.")
        else:
            print(f"Введите значение поля {field_name}. ({field_desc})")
        field_value = input(f"{field_name}: ")
        return field_value

    @staticmethod
    def offer_save_changes() -> str:
        data = input("Есть несохранённые изменения. Сохранить изменения перед выходом? (y/n): ")
        return data

    @staticmethod
    def print_full_contact_info(num: int, contact_info: list[(str, str)]):
        print(f"Запись {num}:")
        for data in contact_info:
            print("{0:>25}: {1:}".format(data[0], data[1]))

    @staticmethod
    def print_brief_contact_info(num:int, name:str, lastname:str, phone:str):
        print(f"Запись {num}: ")
        print(f"{name} {lastname} ")
        print(f"{phone}\n")

    @staticmethod
    def print_error_msg(msg: str):
        print(f">>>{msg}")

    @staticmethod
    def print_info_msg(type_msg: PBVPrintInfoMsgArg):
        if PBVPrintInfoMsgArg.PB_NOT_OPEN == type_msg:
            print(">>>Не открыта телефонная книга")
        elif PBVPrintInfoMsgArg.EMPTY_PB_LIST == type_msg:
            print(">>>В книге пока нет записей")
        elif PBVPrintInfoMsgArg.EMPTY_FIND_LIST == type_msg:
            print(">>>Не нашлись записи по вашему запросу")
        elif PBVPrintInfoMsgArg.SC_OPEN_PB == type_msg:
            print(">>>Книга открыта")
        elif PBVPrintInfoMsgArg.SC_ADD_CONTACT == type_msg:
            print(">>>Контакт добавлен")
        elif PBVPrintInfoMsgArg.SC_SAVED_CHANGES == type_msg:
            print(">>>Изменения сохранены")
        elif PBVPrintInfoMsgArg.SC_CHANGE_CONTACT == type_msg:
            print(">>>Контакт изменён")
        elif PBVPrintInfoMsgArg.SC_DELETE_CONTACT == type_msg:
            print(">>>Контакт удалён")
        elif PBVPrintInfoMsgArg.PB_CLOSE == type_msg:
            print(">>>Телефонная книга закрыта")