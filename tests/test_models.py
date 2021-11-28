import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.models.history import History
from app.models.user import User
import re


# User Class Validation
def validate_password(password):
    assert len(password) >= 8, 'Password must contain at least 8 characters'
    assert re.match(
        '.*[A-Z]+.*', password), 'Password must contain at least one uppercase letter'
    assert re.match(
        '.*[a-z]+.*', password), 'Password must contain at least one lowercase letter'
    assert re.match(
        '.*[0-9]+.*', password), 'Password must contain at least one number'
    assert re.match(
        '.*[!@#$%^&*]+.*', password), 'Password must contain at least one special character [!@#$%^&*]'


@pytest.mark.parametrize("sample_list", [
    ['abc@xyz.net', 'John Smith', '12345!@#Xu'],
    ['zyx@abc.net', 'Jane Doe', 'ABCde1#$%']
])
def test_User_Class(sample_list, capsys):
    with capsys.disabled():
        new_user = User(
            email=sample_list[0],
            username=sample_list[1],
            password=generate_password_hash(sample_list[2], method='sha256')
        )

        assert new_user.email == sample_list[0]
        assert new_user.username == sample_list[1]
        validate_password(sample_list[2])
        assert check_password_hash(new_user.password, sample_list[2])


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize("sample_list", [
    ['aim@arg.org', '', '12345!@#Xu'],
    ['aim@arg.org', 'ethan', ''],
    ['', 'ethan', '12345!@#Xu'],
    ['aim@arg.org', None, '12345!@#Xu'],
    ['aim@arg.org', 'ethan', None],
    [None, 'ethan', '12345!@#Xu']
])
def test_User_Class_Nulls(sample_list, capsys):
    test_User_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize("sample_list", [
    ['abcdefgh', 'Another John', '12345!@#Xu'],
    ['email2@xyz.net', 'John Smith', '12345'],
    ['zyx@abc.net', 'Jane Doe', 'Abcde123']
])
def test_User_Class_Invalid(sample_list, capsys):
    test_User_Class(sample_list=sample_list, capsys=capsys)


# History Class Validation
@pytest.mark.parametrize("sample_list", [
    [1, 50.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [2, 100.0, 4, datetime(1998, 10, 3), 1980, 200_000.0]
])
def test_History_Class(sample_list, capsys):
    with capsys.disabled():
        now = datetime.utcnow()
        new_prediction = History(
            userid=sample_list[0],
            floor_area=sample_list[1],
            bedrooms=sample_list[2],
            approval_date=sample_list[3],
            lease_commencement_year=sample_list[4],
            resale_prediction=sample_list[5],
            predicted_on=now
        )

        assert new_prediction.userid == sample_list[0]
        assert new_prediction.floor_area == sample_list[1]
        assert new_prediction.bedrooms == sample_list[2]
        assert new_prediction.approval_date == sample_list[3]
        assert new_prediction.lease_commencement_year == sample_list[4]
        assert new_prediction.resale_prediction == sample_list[5]
        assert new_prediction.predicted_on == now


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize("sample_list", [
    [None, 50.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, None, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, None, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, 3, None, 1970, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), None, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 1970, None]
])
def test_History_Class_Nulls(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Entries Out of Range')
@pytest.mark.parametrize("sample_list", [
    [1, 0.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 1000.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, 0, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, 5, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, 3, datetime(1000, 10, 3), 1970, 100_000.0],
    [1, 50.0, 3, datetime(2030, 10, 3), 1970, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 1880, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 2020, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 1970, -100.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 1970, 1_000_000.0]
])
def test_History_Class_Out_of_Range(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize("sample_list", [
    [1.1, 50.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    ['1', 50.0, 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, '50.0', 3, datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, '3', datetime(1995, 10, 3), 1970, 100_000.0],
    [1, 50.0, 3, 'datetime(1995, 10, 3)', 1970, 100_000.0],
    [1, 50.0, 3, datetime(1995, 10, 3), 1970.5, 100_000],
    [1, 50.0, 3, datetime(1995, 10, 3), 1970, True],
])
def test_History_Class_Invalid(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)