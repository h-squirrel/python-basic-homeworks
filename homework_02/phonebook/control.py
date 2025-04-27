from phonebook.model import PhoneBookModel, PBMContactFiledName
from phonebook.view import PhoneBookView, PBVPrintInfoMsgArg, PBVGetContactNumArgs

class PhoneBookControl:
    __return_world = 'back'

    def __init__(self, view: PhoneBookView, model:PhoneBookModel):
        self.view = view
        self.model = model

    def __del__(self):
        self.view = None
        self.model = None

    @classmethod
    def __check_is_return_world(cls, world: str):
        return True if cls.__return_world == world else False

    @staticmethod
    def __num_to_idx(num: int) -> int:
        return num - 1
    @staticmethod
    def __idx_to_num(idx: int) -> int:
        return idx + 1

    def __get_contact_num(self, action: PBVGetContactNumArgs) -> int or None:
        result = None
        contact_list_size = self.model.get_contact_list_size()
        if 0 == contact_list_size:
            self.view.print_info_msg(PBVPrintInfoMsgArg.EMPTY_PB_LIST)
            return None
        stop_flag = False
        while not stop_flag:
            data = self.view.get_contact_number(PhoneBookControl.__return_world, action, contact_list_size)
            if PhoneBookControl.__check_is_return_world(data):
                stop_flag = True
            elif data.isdigit():
                num = int(data)
                if (0 < num) and (num <= contact_list_size):
                    result = num
                    stop_flag = True
                else:
                    self.view.print_error_msg(f"В телефонной книге нет записи с номером '{num}'")
        return result

    def __get_field_name(self) -> str or None:
        result = None
        stop_flag = False
        while not stop_flag:
            data = self.view.get_field_name(PhoneBookControl.__return_world)
            if PhoneBookControl.__check_is_return_world(data):
                stop_flag = True
            elif self.model.is_contact_field_name_correct(data):
                result = data
                stop_flag = True
            else:
                self.view.print_error_msg(f"Некорректное поле для записи изменений. В книге нет поля '{data}' для записи")
        return result

    def __get_field_value(self, const_field_name: PBMContactFiledName, field_desc: tuple) -> str or None:
        result = None
        stop_flag = False
        while not stop_flag:
            field_value = self.view.get_field_value(PhoneBookControl.__return_world, field_desc[0], field_desc[1])
            if PhoneBookControl.__check_is_return_world(field_value):
                stop_flag = True
            elif self.model.check_contact_field_value(const_field_name, field_value):
                result = field_value
                stop_flag = True
            else:
                self.view.print_error_msg(f"Некорректное значение поля для записи.")
        return result

    def __show_contact_full_info(self, num: int, contact: dict[str, str]):
        fields_desc = self.model.get_fields_desc_list()
        contact_info = []
        for const_field in fields_desc:
            contact_info.append(
                (fields_desc[const_field][0], contact[self.model.const_to_str_field_name(const_field)]))
        self.view.print_full_contact_info(num, contact_info)

    def open_phonebook(self) -> None:
        try:
            self.model.open_phonebook()
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.view.print_info_msg(PBVPrintInfoMsgArg.SC_OPEN_PB)

    def saved_changes(self) -> None:
        try:
            self.model.save_changes()
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.view.print_info_msg(PBVPrintInfoMsgArg.SC_SAVED_CHANGES)

    def show_all_contacts(self) -> None:
        try:
            contact_list = self.model.get_contact_list()
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            if 0 == len(contact_list):
                self.view.print_info_msg(PBVPrintInfoMsgArg.EMPTY_PB_LIST)
                return None
            field_firstname = self.model.const_to_str_field_name(PBMContactFiledName.FIRST_NAME)
            field_lastname = self.model.const_to_str_field_name(PBMContactFiledName.LAST_NAME)
            field_phone = self.model.const_to_str_field_name(PBMContactFiledName.PHONE)
            for idx, contact in enumerate(contact_list):
                self.view.print_brief_contact_info(PhoneBookControl.__idx_to_num(idx),
                                                   contact[field_firstname], contact[field_lastname], contact[field_phone])

    def show_contact_info(self):
        if not self.model.is_phonebook_open():
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_NOT_OPEN)
            return None
        num = self.__get_contact_num(PBVGetContactNumArgs.SHOW_CONTACT_INFO)
        if num is None:
            return None
        try:
            contact = self.model.get_contact_info(PhoneBookControl.__num_to_idx(num))
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.__show_contact_full_info(num, contact)

    def add_contact(self):
        if not self.model.is_phonebook_open():
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_NOT_OPEN)
            return None
        new_contact = {}
        fields_desc = self.model.get_fields_desc_list()
        for const_field_name, field_desc in fields_desc.items():
            field_value = self.__get_field_value(const_field_name, field_desc)
            if field_value is None:
                return None
            new_contact[const_field_name] = field_value
        try:
            idx, contact = self.model.add_contact(new_contact)
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.view.print_info_msg(PBVPrintInfoMsgArg.SC_ADD_CONTACT)
            self.__show_contact_full_info(PhoneBookControl.__idx_to_num(idx), contact)

    def find_contacts(self):
        if not self.model.is_phonebook_open():
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_NOT_OPEN)
            return None
        data = self.view.get_data_for_find(PhoneBookControl.__return_world)
        if PhoneBookControl.__check_is_return_world(data):
            return None
        try:
            result_contact_list = self.model.find_contacts(data)
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            if 0 == len(result_contact_list):
                self.view.print_info_msg(PBVPrintInfoMsgArg.EMPTY_FIND_LIST)
            else:
                field_firstname = self.model.const_to_str_field_name(PBMContactFiledName.FIRST_NAME)
                field_lastname = self.model.const_to_str_field_name(PBMContactFiledName.LAST_NAME)
                field_phone = self.model.const_to_str_field_name(PBMContactFiledName.PHONE)
                for contact in result_contact_list:
                    self.view.print_brief_contact_info(contact[0], contact[1][field_firstname],
                                                       contact[1][field_lastname], contact[1][field_phone])

    def change_contact(self):
        if not self.model.is_phonebook_open():
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_NOT_OPEN)
            return None
        num = self.__get_contact_num(PBVGetContactNumArgs.CHANGE_CONTACT)
        if num is None:
            return None
        str_field_name = self.__get_field_name()
        if str_field_name is None:
            return None
        const_field_name = self.model.str_to_const_field_name(str_field_name)
        field_desc = self.model.get_field_desc(const_field_name)
        field_value = self.__get_field_value(const_field_name, field_desc)
        if field_value is None:
            return None
        try:
            contact = self.model.edit_contact(PhoneBookControl.__num_to_idx(num), const_field_name, field_value)
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.view.print_info_msg(PBVPrintInfoMsgArg.SC_CHANGE_CONTACT)
            self.__show_contact_full_info(num, contact)

    def delete_contact(self):
        if not self.model.is_phonebook_open():
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_NOT_OPEN)
            return None
        num = self.__get_contact_num(PBVGetContactNumArgs.DELETE_CONTACT)
        if num is None:
            return None
        try:
            contact = self.model.del_contact(PhoneBookControl.__num_to_idx(num))
        except Exception as e:
            self.view.print_error_msg(str(e))
        else:
            self.view.print_info_msg(PBVPrintInfoMsgArg.SC_DELETE_CONTACT)
            self.__show_contact_full_info(num, contact)

    def close_phonebook(self):
        if not self.model.is_phonebook_open():
            return None
        if not self.model.check_exist_changes():
            self.model.close_phonebook()
            self.view.print_info_msg(PBVPrintInfoMsgArg.PB_CLOSE)
            return
        stop_flag = False
        while not stop_flag:
            data = self.view.offer_save_changes()
            if 'y' == data:
                try:
                    self.model.save_changes()
                except Exception as e:
                    self.view.print_error_msg(str(e))
                else:
                    self.view.print_info_msg(PBVPrintInfoMsgArg.SC_SAVED_CHANGES)
                finally:
                    stop_flag = True
            elif 'n' == data:
                stop_flag = True
        self.model.close_phonebook()
        self.view.print_info_msg(PBVPrintInfoMsgArg.PB_CLOSE)