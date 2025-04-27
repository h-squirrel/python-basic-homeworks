class PBErrors(Exception):
    default_msg = "Ошибка при работе с телефонной книгой"

    def __init__(self, msg = None):
        self.msg = self.default_msg if msg is None else msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Error: {self.msg}"

class PBDataFileError(PBErrors):
    default_msg = "Файл телефонной книги повреждён: некорректный формат данных"

class PBReopeningError(PBErrors):
    default_msg = "Телефонная книга уже открыта"

class PBNoOpenBookFoundError(PBErrors):
    default_msg = "Телефонная книга не открыта. Нет доступа к записям."

class PBEntryIdxError(PBErrors):
    default_msg = "В книге нет записи с указанным идентификатором."

class PBFieldSetError(PBErrors):
    default_msg = "Недостаточно данных для добавления контакта. Переданы не все поля для записи"

class PBFieldValueError(PBErrors):
    default_msg = "Некорректные значения полей записи"

class PBFieldNameError(PBErrors):
    default_msg = "Не существует указанного поля для записи"

class PBExistChangesError(PBErrors):
    default_msg = "Нет изменений для сохранения"