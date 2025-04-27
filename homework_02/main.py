import os
import sys
sys.path.append(os.getcwd())

from phonebook.model import PhoneBookModel
from phonebook.view import PhoneBookView
from phonebook.control import PhoneBookControl

def phonebook_menu_print() -> None:
    menu_file = open('menu.txt', 'r+', encoding='utf-8')
    for menu_item in menu_file:
        print(menu_item.rstrip("\n"))
    menu_file.close()

def main():
    model = PhoneBookModel()
    view = PhoneBookView()
    control = PhoneBookControl(view, model)

    phonebook_menu_print()
    stop_flag = False
    while not stop_flag:
        data = input("Выберите пункт меню (1-9). Для повторного показа меню введите 0: ")
        if not data.isdigit():
            continue
        action = int(data)
        if 0 == action:
            phonebook_menu_print()
        elif 1 == action:
            control.open_phonebook()
        elif 2 == action:
            control.saved_changes()
        elif 3 == action:
            control.show_all_contacts()
        elif 4 == action:
            control.show_contact_info()
        elif 5 == action:
            control.add_contact()
        elif 6 == action:
            control.find_contacts()
        elif 7 == action:
            control.change_contact()
        elif 8 == action:
            control.delete_contact()
        elif 9 == action:
            control.close_phonebook()
            stop_flag = True
    del control
    del model
    del view

if __name__ == '__main__':
    main()