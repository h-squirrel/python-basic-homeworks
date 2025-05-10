import pytest

from phonebook.errors import PBExistChangesError, PBNoOpenBookFoundError
from phonebook.model import PhoneBookModel
from tests.test_data import test_add_contact_data, test_del_contact_data, test_edit_contact_data
from tests.test_data import TestSavedChangesMode, test_saved_changes_data, CONTACT_LIST_SIZE


@pytest.mark.parametrize('data, result', test_add_contact_data)
def test_add_contact(data, result):
    PhoneBookModel.phonebook_file_name = "phonebook.json"
    model = PhoneBookModel()
    model.open_phonebook()
    try:
        idx_new_contact, new_contact = model.add_contact(data)
    except Exception as e:
        assert str(e) == result
    else:
        assert (idx_new_contact, new_contact) == result

@pytest.mark.parametrize('data, result', test_del_contact_data)
def test_del_contact(data, result):
    model = PhoneBookModel()
    model.phonebook_file_name = "phonebook.json"
    model.open_phonebook()
    try:
        del_contact = model.del_contact(data)
    except Exception as e:
        assert str(e) == result
    else:
        assert (model.change_flag, del_contact) == result

@pytest.mark.parametrize('data, result', test_edit_contact_data)
def test_edit_contact(data, result):
    PhoneBookModel.phonebook_file_name = "phonebook.json"
    model = PhoneBookModel()
    model.open_phonebook()
    try:
        edit_contact = model.edit_contact(data[0], data[1], data[2])
    except Exception as e:
        assert str(e) == result
    else:
        assert edit_contact == result

@pytest.fixture(scope='function')
def rollback_changes_after_test():
    fixture_model: list[PhoneBookModel] = []
    fixture_data: list[bool] = [False]

    def _model_prepare(mode):
        PhoneBookModel.phonebook_file_name = "phonebook.json"
        model = PhoneBookModel()
        if TestSavedChangesMode.CHANGES_Y == mode:
            model.open_phonebook()
            model.add_contact(test_add_contact_data[0][0])
            fixture_data[0] = True
        elif TestSavedChangesMode.CHANGES_N == mode:
            model.open_phonebook()
        fixture_model.append(model)
        return model

    yield _model_prepare

    if fixture_data[0]:
        for i in range(CONTACT_LIST_SIZE, fixture_model[0].get_contact_list_size()):
            fixture_model[0].del_contact(i)
        fixture_model[0].save_changes()
    del fixture_model[0]

@pytest.mark.parametrize('data, result', test_saved_changes_data)
def test_saved_changes(rollback_changes_after_test, data, result):
    model = rollback_changes_after_test(data)
    try:
        model.save_changes()
    except PBExistChangesError:
        assert str(PBExistChangesError()) == result
    except PBNoOpenBookFoundError:
        assert str(PBNoOpenBookFoundError()) == result
    except Exception as e:
        assert str(e) == "Error"
    else:
        assert model.change_flag == result