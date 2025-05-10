from enum import Enum
# импорты из проекта
from phonebook.model import PBMContactFiledName


CONTACT_LIST_SIZE = 5

test_add_contact_results = [
    (CONTACT_LIST_SIZE, {"phone": "+-0123456789", "name": "Test", "lastname": "TestTest", "birthday": "10.05.2025", "note": "test123 +-/.,;'@#$%^&*()__++=qq "}),
    "Error: Некорректные значения полей записи", #PBFieldValueError
    (CONTACT_LIST_SIZE, {"phone": "+-0123456789", "name": "+-0123456789", "lastname": "", "birthday": "", "note": ""}),
    "Error: Некорректные значения полей записи", #PBFieldValueError
    "Error: Некорректные значения полей записи", #PBFieldValueError
    "Error: Некорректные значения полей записи", #PBFieldValueError
    (CONTACT_LIST_SIZE, {"phone": "+-0123456789", "name": "", "lastname": "TestTest", "birthday": "10/05/2025", "note": ""}),
]
test_add_contact_data = [
    ({
        # Success test
        PBMContactFiledName.PHONE: "+-0123456789",
        PBMContactFiledName.FIRST_NAME: "Test",
        PBMContactFiledName.LAST_NAME: "TestTest",
        PBMContactFiledName.BIRTHDAY: "10.05.2025",
        PBMContactFiledName.NOTE: "test123 +-/.,;'@#$%^&*()__++=qq ",
    }, test_add_contact_results[0]),
    ({
        # Error phone data test
        PBMContactFiledName.PHONE: "q",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "",
        PBMContactFiledName.BIRTHDAY: "",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[1]),
    ({
        # Success test
        PBMContactFiledName.PHONE: "+-0123456789",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "",
        PBMContactFiledName.BIRTHDAY: "",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[2]),
    ({
        # Error phone data test
        PBMContactFiledName.PHONE: "",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "",
        PBMContactFiledName.BIRTHDAY: "",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[3]),
    ({
        # Error birthday data test
        PBMContactFiledName.PHONE: "+-0123456789",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "",
        PBMContactFiledName.BIRTHDAY: "10/05.2025",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[4]),
    ({
        # Error birthday data test
        PBMContactFiledName.PHONE: "+-0123456789",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "",
        PBMContactFiledName.BIRTHDAY: "10.05/2025",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[5]),
    ({
        # Success test
        PBMContactFiledName.PHONE: "+-0123456789",
        PBMContactFiledName.FIRST_NAME: "",
        PBMContactFiledName.LAST_NAME: "TestTest",
        PBMContactFiledName.BIRTHDAY: "10/05/2025",
        PBMContactFiledName.NOTE: "",
    }, test_add_contact_results[6])
]

test_del_contact_result = [
    (True, {"phone": "+7 812 507-07-77", "name": "+7 812 507-07-77", "lastname": "", "birthday": "", "note": "Велодрайв на Академке"}),
    "Error: В книге нет записи с указанным идентификатором." # PBEntryIdxError
]

test_del_contact_data = [
    # Success test
    (1, test_del_contact_result[0]),
    # Error test
    (50, test_del_contact_result[1])
]

test_edit_contact_result = [
    "Error: Некорректные значения полей записи", # PBFieldValueError
    {
        "phone": "+7 812 507-07-77",
        "name": "",
        "lastname": "TestTest",
        "birthday": "",
        "note": "Велодрайв на Академке"
    }
]

test_edit_contact_data = [
    # Не указан номер телефона, ожидаем ошибку
    ((1, PBMContactFiledName.PHONE, ""), test_edit_contact_result[0]),
    #  Записываем Фималию контакт, вместо пустой строки. Должен пропасть номер телефона из поля "name"
    ((1, PBMContactFiledName.LAST_NAME, "TestTest"), test_edit_contact_result[1]),
]

class TestSavedChangesMode(Enum):
    PB_OPEN_N  = 0 # Книга не открыта
    CHANGES_N  = 1 # Книга открыта, нет изменений для сохранения
    CHANGES_Y  = 2 # Книга открыта, есть изменения для сохранения

test_saved_changes_result = [
    "Error: Телефонная книга не открыта. Нет доступа к записям.", # PBNoOpenBookFoundError
    "Error: Нет изменений для сохранения", # PBExistChangesError
    False # Значение флага наличия изменений после сохранения изменений
]

test_saved_changes_data = [
    (TestSavedChangesMode.PB_OPEN_N, test_saved_changes_result[0]),
    (TestSavedChangesMode.CHANGES_N, test_saved_changes_result[1]),
    (TestSavedChangesMode.CHANGES_Y, test_saved_changes_result[2])
]