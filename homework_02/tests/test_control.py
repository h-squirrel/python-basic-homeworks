import os
import sys
sys.path.append(os.getcwd())

from phonebook.control import PhoneBookControl
from phonebook.model import PhoneBookModel
from phonebook.view import PhoneBookView


def test_open_pb_success(capfd):
    PhoneBookModel.phonebook_file_name = "phonebook.json"
    model = PhoneBookModel()
    view = PhoneBookView()
    control = PhoneBookControl(view, model)
    control.open_phonebook()
    out, err = capfd.readouterr()
    assert out == ">>>Книга открыта\n"

def test_open_pb_failed(capfd):
    PhoneBookModel.phonebook_file_name = "pb.json"
    model = PhoneBookModel()
    view = PhoneBookView()
    control = PhoneBookControl(view, model)
    control.open_phonebook()
    out, err = capfd.readouterr()
    assert out == f">>>[Errno 2] No such file or directory: '{PhoneBookModel.phonebook_file_name}'\n"