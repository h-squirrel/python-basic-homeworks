from phonebook import errors
from json import load, dumps
from re import compile, search
from enum import Enum

class PBMContactFiledName(Enum):
    PHONE      = 0
    FIRST_NAME = 1
    LAST_NAME  = 2
    BIRTHDAY   = 3
    NOTE       = 4

class PhoneBookModel:
    phonebook_file_name = "phonebook.json"
    phonebook_key_contact_list = "phonebook"
    __phonebook_contact_field_name_set = ("phone", "name", "lastname", "birthday", "note")
    __phonebook_contact_fields_description =\
        {
            PBMContactFiledName.PHONE: ("Номер телефона", "Допустимые символы - 0-9,+,-"),
            PBMContactFiledName.FIRST_NAME: ("Имя", ""),
            PBMContactFiledName.LAST_NAME: ("Фамилия", ""),
            PBMContactFiledName.BIRTHDAY: ("День рождения", "Дата в формате DD/MM/YYYY или DD.MM.YYYY"),
            PBMContactFiledName.NOTE: ("Комментарий", "")
        }

    def __init__(self):
        self.phonebook_dict = {}
        self.contact_list = []
        self.change_flag = False


    def __del__(self):
        self.contact_list = None
        self.phonebook_dict = None


    @classmethod
    def get_fields_desc_list(cls) -> dict:
        return cls.__phonebook_contact_fields_description

    @classmethod
    def get_field_desc(cls, field_name: PBMContactFiledName) -> tuple:
        return cls.__phonebook_contact_fields_description[field_name]

    @classmethod
    def is_contact_field_name_correct(cls, field_name: str) -> bool:
        return True if field_name in cls.__phonebook_contact_field_name_set else False

    @classmethod
    def const_to_str_field_name(cls, const_field_name: PBMContactFiledName) -> str:
        return cls.__phonebook_contact_field_name_set[const_field_name.value]

    @classmethod
    def str_to_const_field_name(cls, str_field_name: str) -> PBMContactFiledName:
        idx = PhoneBookModel.__phonebook_contact_field_name_set.index(str_field_name)
        return PBMContactFiledName(idx)

    @staticmethod
    def __check_phone_data(data: str) -> bool:
        if "" == data:
            return False
        return True if search( r'[^-+\d\s]', data) is None else False

    @staticmethod
    def __check_birthday_data(data: str) -> bool:
        pattern = compile(r'^\s*\d\d([./])\d\d\1\d{4}\s*$')
        return False if (data != "") and (not pattern.match(data)) else True

    @classmethod
    def check_contact_field_value(cls, field_name: PBMContactFiledName, field_value: str) -> bool:
        if PBMContactFiledName.PHONE == field_name:
            return cls.__check_phone_data(field_value)
        elif PBMContactFiledName.BIRTHDAY == field_name:
            return cls.__check_birthday_data(field_value)
        elif (PBMContactFiledName.FIRST_NAME == field_name) or (PBMContactFiledName.LAST_NAME == field_name) or (PBMContactFiledName.NOTE == field_name):
            return True
        return False

    def is_phonebook_open(self) -> bool:
        return False if 0 == len(self.phonebook_dict) else True

    def check_exist_changes(self) -> bool:
        return self.change_flag

    def check_contact_idx(self, idx) -> bool:
        if 0 == len(self.contact_list):
            return False
        return True if (0 <= idx) and (idx < len(self.contact_list)) else False

    def get_contact_list_size(self) -> int:
        return len(self.contact_list)

    def open_phonebook(self) -> None:
        if self.is_phonebook_open():
            raise pb_errors.PBReopeningError()
        with open(self.phonebook_file_name, "r", encoding='utf-8') as phonebook_file:
            json_data: dict = load(phonebook_file)
            if not PhoneBookModel.phonebook_key_contact_list in json_data:
                raise pb_errors.PBDataFileError()
            self.phonebook_dict = json_data
            self.contact_list = self.phonebook_dict[PhoneBookModel.phonebook_key_contact_list]

    def close_phonebook(self):
        self.phonebook_dict = {}
        self.contact_list = []
        self.change_flag = False

    def save_changes(self) -> None:
        if not self.is_phonebook_open():
            raise pb_errors.PBNoOpenBookFoundError()
        if not self.change_flag:
            raise pb_errors.PBExistChangesError()
        with open(self.phonebook_file_name, "w", encoding='utf-8') as phonebook_file:
            phonebook_file.write(dumps(self.phonebook_dict, indent=4, ensure_ascii=False))
            self.change_flag = False

    def get_contact_list(self) -> list[dict[str, str]]:
        if not self.is_phonebook_open():
            raise pb_errors.PBNoOpenBookFoundError()
        return self.contact_list

    def get_contact_info(self, idx: int) -> dict[str, str]:
        if not self.is_phonebook_open():
            raise pb_errors.PBNoOpenBookFoundError()
        if not self.check_contact_idx(idx):
            raise pb_errors.PBEntryIdxError()
        return self.contact_list[idx]

    def add_contact(self, contact: dict[PBMContactFiledName, str]) -> (int, dict[str, str]):
        if not self.is_phonebook_open():
            raise pb_errors.PBNoOpenBookFoundError()
        for key in PhoneBookModel.__phonebook_contact_fields_description:
            if not key in contact:
                raise pb_errors.PBFieldSetError()
        for field_name, field_value in contact.items():
            if not PhoneBookModel.check_contact_field_value(field_name, field_value):
                raise pb_errors.PBFieldValueError()
        new_contact = {}
        for key in PhoneBookModel.__phonebook_contact_fields_description:
            new_contact[PhoneBookModel.const_to_str_field_name(key)] = contact[key]
        if ("" == new_contact["name"]) and ("" == new_contact["lastname"]):
            new_contact["name"] = new_contact["phone"]
        elif ((new_contact['name'] == new_contact['phone']) and
              ("" != new_contact['lastname'])):
            new_contact['name'] = ""
        new_contact_idx = len(self.contact_list)
        self.contact_list.append(new_contact)
        self.change_flag = True
        return new_contact_idx, self.contact_list[new_contact_idx]

    def find_contacts(self, data: str) -> list[(int, dict[str, str])]:
        result_list = []
        for idx, contact in enumerate(self.contact_list):
            if (data in contact['phone']) or (data in contact['name']) or (data in contact['lastname']):
                result_list.append((idx, contact))
        return result_list

    def edit_contact(self, idx: int, const_field_name: PBMContactFiledName, field_value: str) -> dict[str, str]:
        if not self.check_contact_idx(idx):
            raise pb_errors.PBEntryIdxError()
        str_field_name = PhoneBookModel.const_to_str_field_name(const_field_name)
        if not PhoneBookModel.is_contact_field_name_correct(str_field_name):
            raise pb_errors.PBFieldNameError()
        if 'phone' == str_field_name:
            if not PhoneBookModel.__check_phone_data(field_value):
                raise pb_errors.PBFieldValueError()
        elif 'birthday' == str_field_name:
            if not PhoneBookModel.__check_birthday_data(field_value):
                raise pb_errors.PBFieldValueError()
        self.contact_list[idx][str_field_name] = field_value
        if ("" == self.contact_list[idx]['lastname']) and ("" == self.contact_list[idx]['name']):
            self.contact_list[idx]['name'] = self.contact_list[idx]['phone']
        elif ((self.contact_list[idx]['name'] == self.contact_list[idx]['phone']) and
              ("" != self.contact_list[idx]['lastname'])):
            self.contact_list[idx]['name'] = ""
        self.change_flag = True
        return self.contact_list[idx]

    def del_contact(self, idx) -> dict[str, str]:
        if not self.check_contact_idx(idx):
            raise pb_errors.PBEntryIdxError()
        contact =  self.contact_list.pop(idx)
        self.change_flag = True
        return contact