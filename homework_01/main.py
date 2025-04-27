import json
import re

CONST_PB_FILE_NAME = 'phone_book.json'
CONST_PBA_MENU_FILE_NAME = 'menu.txt'
CONST_PBA_RETURN_WORLD = 'back'
global_pba_str_dict = \
    {
        'pb_get_action': "Выберите пункт меню. Для повторного показа меню введите 0: ",
        'pb_back_info': f"Для возврата в главное меню введите '{CONST_PBA_RETURN_WORLD}'",
        'pb_change_print': "Введите новое значение для выбранного поля записи: ",
        'pb_entry_info_get_num': "Введите номер записи, которую хотите просмотреть: ",
        'pb_del_get_num': "Введите номер записи, которую хотите удалить: ",
        'pb_change_get_num': "Введите номер записи, которую хотите изменить: ",
        'pb_change_get_field': "Какое поле записи вы хотите изменить (phone, name, lastname, birthday, note): ",
        'pb_find_entries': "Введите данные для поиска: ",
        'pb_get_phone': "Номер телефона (допустимые символы номера: 0-9, +, -): ",
        'pb_get_name': "Имя: ",
        'pb_get_lastname': "Фамилия: ",
        'pb_get_birthday': "День рождения (в формате DD.MM.YYYY или DD/MM/YYYY или оставьте строку пустой): ",
        'pb_get_note': "Комментарий: ",
        'pb_changes_quest': "Введите \'y\', если хотите изменить другие поля выбранной записи: ",
        'pb_offer_to_save': "Есть несохранённые измменения. "
                             "Введите \'y\' чтобы сохранить изменения перед завершением работы с ассистентом: ",
        'pb_exit': "Работа с ассистентом записной книги завершена",
        'pb_open_success': ">>> Телефонная книга успешно открыта",
        'pb_save_changes_y': ">>> Все изменения сохранены",
        'pb_save_changes_n': ">>> Нет изменений для сохранения",
        'pb_del_entry': "Запись успешно удалена",
        'pb_change_entry': "Запись успешно изменена",
        'pb_add_entry': "Запись успешно добавлена",
        'pb_already_open': "Телефонная книга уже открыта",
        'pb_get_phone_err': ">>>Некорректный номер телефона. (Допустимые символы номера: 0-9, +, -)",
        'pb_get_birthday_err': ">>>Некорректный формат даты. Укажите дату в формате: DD.MM.YYYY или DD/MM/YYYY",
        'pb_find_entries_err': ">>> По вашему запросу не нашлась ни одна запись",
        'pb_get_entry_num_err': lambda num, l: f">>> Записи с номером {num} не существует. Кол-во записей в книге - {l}",
        'pb_param_err': ">>>Извините, выбранное действие сейчас недоступно. Неизвестная ошибка.",
        'pb_data_none_err': ">>>Нет данных. Пожалуйста, откройте телефонную книгу и попробуйте снова.",
        'pb_fdata_file_err': ">>>Выбранное действие недоступно. Повреждён файл записей телефонной книги - некорректный формат данных."
    }


def check_pb_data(function):
    def check(*args):
        tuple_fields = ("phone", "name", "lastname", "birthday", "note")
        if args[0]['data'] is None:
            print(global_pba_str_dict['pb_data_none_err'])
            return None
        if not 'phonebook' in args[0]['data']:
            print(global_pba_str_dict['pb_fdata_file_err'])
            return None
        for entry in args[0]['data']['phonebook']:
            for field in tuple_fields:
                if not field in entry:
                    print(global_pba_str_dict['pb_fdata_file_err'])
                    return None
        function(*args)
    return check

@check_pb_data
def offer_to_save(pb_dict: dict):
    data = input(global_pba_str_dict['pb_offer_to_save'])
    if "y" == data:
        phone_book_save_changes(pb_dict)

check_back_to_menu = lambda dt: True if CONST_PBA_RETURN_WORLD == dt else False

def print_entry_full_info(entry: dict, entry_num: int):
    print(f"Номер записи: {entry_num}:")
    print(f"    Номер: {entry['phone']}")
    print(f"    Имя: {entry['name']}")
    print(f"    Фамилия: {entry['lastname']}")
    print(f"    День рождения: {entry['birthday']}")
    print(f"    Комментарий: {entry['note']}")

def print_entry_brief_info(entry: dict, entry_num: int):
    print(f'Номер записи - {entry_num}:')
    print(f'    Контакт: {entry["name"]} {entry["lastname"]}')
    print(f'    Номер: {entry["phone"]}\n')

def get_phone() -> (bool, str):
    data: str = ""
    get_data_success_flag = False
    stop_flag = False
    while not stop_flag:
        print(global_pba_str_dict['pb_back_info'])
        data = input(global_pba_str_dict['pb_get_phone'])
        if check_back_to_menu(data):
            stop_flag = True
        elif not re.search( r'[^-\d\s\+]', data) is None:
            print(global_pba_str_dict['pb_get_phone_err'])
        else:
            get_data_success_flag = True
            stop_flag = True
    return get_data_success_flag, data

def get_birthday() -> str:
    data = ""
    stop_flag = False
    while not stop_flag:
        data = input(global_pba_str_dict['pb_get_birthday'])
        pattern = re.compile(r'^\s*\d\d([./])\d\d\1\d{4}\s*$')
        if ("" != data) and (not pattern.match(data)):
            print(global_pba_str_dict['pb_get_birthday_err'])
        else:
            stop_flag = True
    return data

def get_entry_num(entry_list_size: int, request_str_key: str) -> int:
    entry_num = 0
    stop_flag = False
    while not stop_flag:
        print(global_pba_str_dict['pb_back_info'])
        data = input(global_pba_str_dict[request_str_key])
        if data.isdigit():
            entry_num = int(data)
            if (entry_list_size < entry_num) or (entry_num < 1):
                print(global_pba_str_dict['pb_get_entry_num_err'](entry_num, entry_list_size))
                continue
            stop_flag = True
        elif check_back_to_menu(data):
            entry_num = 0
            stop_flag = True
    return entry_num

def get_field() -> (bool, str):
    tuple_keys = ('phone', 'name', 'lastname', 'birthday', 'note')
    data = ""
    get_data_success_flag = False
    stop_flag = False
    while not stop_flag:
        print(global_pba_str_dict['pb_back_info'])
        data = input(global_pba_str_dict['pb_change_get_field'])
        if check_back_to_menu(data):
            stop_flag = True
        elif data in tuple_keys:
            get_data_success_flag = True
            stop_flag = True
    return get_data_success_flag, data

def edit_entry(phonebook: dict, idx: int, field: str) -> bool:
    if 'phone' == field:
        r_bool, data = get_phone()
        if not r_bool:
            return False
        else:
            phonebook[idx][field] = data
            return True
    elif 'birthday' == field:
        data = get_birthday()
        phonebook[idx][field] = data
        return True
    else:
        data = input(global_pba_str_dict['pb_change_print'])
        phonebook[idx][field] = data
    if '' == phonebook[idx]['name'] and '' == phonebook[idx]['lastname']:
        phonebook[idx]['name'] = phonebook[idx]['phone']
    return True

#-----------------------------------------------------------------------------------

def phone_book_menu_print(*args):
    menu_file = open(CONST_PBA_MENU_FILE_NAME, 'r+', encoding='utf-8')
    for menu_item in menu_file:
        print(menu_item.rstrip("\n"))
    menu_file.close()

def phone_book_open_file(pb_dict: dict):
    if pb_dict['data'] is None:
        phone_book_file = open(CONST_PB_FILE_NAME, 'r+', encoding = 'utf-8')
        try:
            data_json = json.load(phone_book_file)
        except Exception as err:
            print(global_pba_str_dict['pb_fdata_file_err'])
            print(err)
        else:
            pb_dict['data'] = data_json
            print(global_pba_str_dict['pb_open_success'])
        finally:
            phone_book_file.close()
    else:
        print(global_pba_str_dict['pb_already_open'])

@check_pb_data
def phone_book_save_changes(pb_dict: dict):
    if pb_dict['change_flag']:
        with open(CONST_PB_FILE_NAME, "w", encoding='utf-8') as phone_book_file:
            phone_book_file.write(json.dumps(pb_dict['data'], indent=4, ensure_ascii=False))
            print(global_pba_str_dict['pb_save_changes_y'])
            pb_dict['change_flag'] = False
    else:
        print(global_pba_str_dict['pb_save_changes_n'])

@check_pb_data
def phone_book_show_all_entries(pb_dict: dict):
    print(f"Записей в книге - {len(pb_dict['data']['phonebook'])}\n")
    for idx, entry in enumerate(pb_dict['data']['phonebook']):
        print_entry_brief_info(entry, idx+1)

@check_pb_data
def phone_book_show_entry_info(pb_dict: dict):
    entry_num = get_entry_num(len(pb_dict['data']['phonebook']), 'pb_entry_info_get_num')
    if 0 == entry_num:
        return
    entry = pb_dict['data']['phonebook'][entry_num - 1]
    print_entry_full_info(entry, entry_num)

@check_pb_data
def phone_book_add_entry(pb_dict: dict):
    res_bool, phone = get_phone()
    if not res_bool:
        return
    name = input(global_pba_str_dict['pb_get_name'])
    lastname = input(global_pba_str_dict['pb_get_lastname'])
    if '' == name and '' == lastname:
        name = phone
    birthday = get_birthday()
    note = input(global_pba_str_dict['pb_get_note'])
    new_entry = {'phone': phone, 'name': name, 'lastname':lastname, 'birthday': birthday, 'note':note}
    pb_dict['data']['phonebook'].append(new_entry)
    pb_dict['change_flag'] = True
    print_entry_full_info(new_entry, len(pb_dict['data']['phonebook']))
    print(global_pba_str_dict['pb_add_entry'])


@check_pb_data
def phone_book_find_entry(pb_dict: dict):
    print(global_pba_str_dict['pb_back_info'])
    data = input(global_pba_str_dict['pb_find_entries'])
    if check_back_to_menu(data):
        return
    if '' == data:
        print(global_pba_str_dict['pb_find_entries_err'])
        return
    found_entry_cnt = 0
    for idx, entry in enumerate(pb_dict['data']['phonebook']):
        if (data in entry['name']) or (data in entry['lastname'])  or (data in entry['phone']):
            print_entry_brief_info(entry, idx + 1)
            found_entry_cnt += 1
    if 0 == found_entry_cnt:
        print(global_pba_str_dict['pb_find_entries_err'])


@check_pb_data
def phone_book_edit_entry(pb_dict: dict):
    entry_s_num = get_entry_num(len(pb_dict['data']['phonebook']), 'pb_change_get_num')
    if 0 == entry_s_num:
        return
    print_entry_full_info(pb_dict['data']['phonebook'][entry_s_num - 1], entry_s_num)
    stop_flag = False
    while not stop_flag:
        res_bool, field = get_field()
        if not res_bool:
            stop_flag = True
            continue
        if not edit_entry(pb_dict['data']['phonebook'], entry_s_num-1, field):
            stop_flag = True
            continue
        pb_dict['change_flag'] = True
        print(global_pba_str_dict['pb_change_entry'])
        print_entry_full_info(pb_dict['data']['phonebook'][entry_s_num - 1], entry_s_num)
        data = input(global_pba_str_dict['pb_changes_quest'])
        if not "y" == data:
            stop_flag = True

@check_pb_data
def phone_book_del_entry(pb_dict: dict):
    entry_s_num = get_entry_num(len(pb_dict['data']['phonebook']), 'pb_del_get_num')
    if 0 == entry_s_num:
        return
    print_entry_full_info(pb_dict['data']['phonebook'][entry_s_num - 1], entry_s_num)
    del pb_dict['data']['phonebook'][entry_s_num - 1]
    pb_dict['change_flag'] = True
    print(global_pba_str_dict['pb_del_entry'])

def phone_book_assistant_stop(pb_dict: dict):
    if pb_dict['change_flag']:
        offer_to_save(pb_dict)
    print(global_pba_str_dict['pb_exit'])

#-----------------------------------------------------------------------------------
def phonebook_assistant_get_action() -> int:
    action = -1
    while (action < 0) or (9 < action):
        num = input(global_pba_str_dict['pb_get_action'])
        if not num.isdigit():
            continue
        action = int(num)
    return action

phone_assistant_dict = {
    0: phone_book_menu_print,
    1: phone_book_open_file,
    2: phone_book_save_changes,
    3: phone_book_show_all_entries,
    4: phone_book_show_entry_info,
    5: phone_book_add_entry,
    6: phone_book_find_entry,
    7: phone_book_edit_entry,
    8: phone_book_del_entry,
    9: phone_book_assistant_stop
}

def phone_book_assistant_start() -> None:
    phone_book_data = None
    pb_dict =\
        {
            'data': phone_book_data,
            'change_flag': False
        }

    phone_book_menu_print()
    stop_flag = False
    while not stop_flag:
        action = phonebook_assistant_get_action()
        phone_assistant_dict[action](pb_dict)
        if 9 == action:
            stop_flag = True
            continue

phone_book_assistant_start()