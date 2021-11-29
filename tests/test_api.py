from datetime import datetime
import json
from flask.json import jsonify
import pytest
from werkzeug.security import check_password_hash
from app.api import new_prediction
from app import output_boundaries, input_boundaries


# New User API
@pytest.mark.parametrize('sample_list', [
    ['ethan@gmail.com', 'Ethan', '12345Abc#', 1],
    ['john@abc.net', 'Doe', '12345^32Jm', 2],
    ['jane@abc.net', 'J', '12345^32Jm', 3],
    ['joe@abc.net', 'Joe', '12345^32Jm', 4]
])
def test_add_new_user_api(client, sample_list, capsys):
    assert type(sample_list[0]) is str
    assert type(sample_list[1]) is str
    assert type(sample_list[2]) is str

    data = json.dumps({
        'email': sample_list[0],
        'username': sample_list[1],
        'password': sample_list[2]
    })
    response = client.post('/api/user/add',
                           json=data,
                           content_type='application/json'
                           )

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    new_user_id = json.loads(response.get_data(as_text=True))['new_user_id']
    assert int(new_user_id) == sample_list[3]


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    ['invalidemail', 'John', '12345Abc#', 2],
    ['valid@email.org', 127, '12345Abc#', 2],
    ['valid@email.org', 'Ethan', '1111111', 2]
])
def test_add_new_user_api_invalid(client, sample_list, capsys):
    test_add_new_user_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize('sample_list', [
    [None, 'John', '12345Abc#', 2],
    ['valid@email.org', None, '12345Abc#', 2],
    ['valid@email.org', 'a user', None, 2]
])
def test_add_new_user_api_nulls(client, sample_list, capsys):
    test_add_new_user_api(
        client=client, sample_list=sample_list, capsys=capsys)

@pytest.mark.xfail(strict=True, reason='Duplicate Entries')
@pytest.mark.parametrize('sample_list', [
    ['ethan@gmail.com', 'John', '12345Abc#', 2],
    ['valid@email.org', 'Ethan', '12345Abc#', 2],
    ['valid@email.org', 'Ethan', 'mdqpdl129(20L', 2]
])
def test_add_new_user_api_duplicates(client, sample_list, capsys):
    test_add_new_user_api(
        client=client, sample_list=sample_list, capsys=capsys)

# Get User API
@pytest.mark.parametrize('sample_list', [
    [1, 'ethan@gmail.com', 'Ethan', '12345Abc#'],
    [2, 'john@abc.net', 'Doe', '12345^32Jm'],
    [3, 'jane@abc.net', 'J', '12345^32Jm'],
    [4, 'joe@abc.net', 'Joe', '12345^32Jm']
])
def test_get_user_api(client, sample_list, capsys):
    with capsys.disabled():
        response = client.get(f'/api/user/get/{sample_list[0]}')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        user = json.loads(response.get_data(as_text=True))
        assert user['id'] == sample_list[0]
        assert user['email'] == sample_list[1]
        assert user['username'] == sample_list[2]
        assert check_password_hash(user['password'], sample_list[3])

@pytest.mark.xfail(strict=True, reason='Non-existent User')
@pytest.mark.parametrize('sample_list', [
    [5, 'ethan@gmail.com', 'Ethan', '12345Abc#']
])
def test_get_user_api_nulls(client, sample_list, capsys):
    test_get_user_api(client, sample_list, capsys)


# New Prediction API
@pytest.mark.parametrize('sample_list', [
    [100.0, 3, datetime(1995, 10, 10), 1970],
    [55.5, 2, datetime(1990, 8, 8), 1967]
])
def test_new_prediction_api(client, sample_list, capsys):
    with capsys.disabled():
        data = json.dumps({
            'floor_area': sample_list[0],
            'bedrooms': sample_list[1],
            'approval_date': datetime.strftime(sample_list[2], '%Y-%m-%d'),
            'lease_commencement_year': sample_list[3]
        })
        response = client.post('/api/predict',
                               data=data,
                               content_type='application/json')

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        resale_pred = json.loads(response.get_data(as_text=True))[
            "resale_pred"]

        assert input_boundaries.loc['min',
                                    'floor_area_sqm'] <= sample_list[0] <= input_boundaries.loc['max', 'floor_area_sqm']
        assert input_boundaries.loc['min',
                                    'bedrooms'] <= sample_list[1] <= input_boundaries.loc['max', 'bedrooms']
        assert input_boundaries.loc['min',
                                    'approval_date'] <= sample_list[2] <= input_boundaries.loc['max', 'approval_date']
        assert input_boundaries.loc['min', 'lease_commencement_year'] <= sample_list[
            3] <= input_boundaries.loc['max', 'lease_commencement_year']
        assert output_boundaries['min'] <= resale_pred <= output_boundaries['max']
        assert new_prediction(
            sample_list[0], sample_list[1], sample_list[2], sample_list[3]) == resale_pred
    return resale_pred


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize('sample_list', [
    [None, 3, datetime(1995, 10, 10), 1970],
    [100.0, None, datetime(1995, 10, 10), 1970],
    [100.0, 3, None, 1970],
    [100.0, 3, datetime(1995, 10, 10), None]
])
def test_new_prediction_api_nulls(client, sample_list, capsys):
    test_new_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    ['str', 3, datetime(1995, 10, 10), 1970],
    [100.0, 'bedrooms', datetime(1995, 10, 10), 1970],
    [100.0, 3, 'date', 1970],
    [100.0, 3, datetime(1995, 10, 10), '']
])
def test_new_prediction_api_invalid(client, sample_list, capsys):
    test_new_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    [-0.0, 3, datetime(1995, 10, 10), 1970],
    [100.0, 5, datetime(1995, 10, 10), 1970],
    [100.0, 3, datetime(2000, 12, 12), 1970],
    [100.0, 3, datetime(1995, 10, 10), 1880]
])
def test_new_prediction_api_out_of_range(client, sample_list, capsys):
    test_new_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


# Store Prediction API
@pytest.mark.parametrize('sample_list', [
    [2, 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0, 1],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 2],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3]
])
def test_store_prediction_api(client, sample_list, capsys):
    with capsys.disabled():
        assert type(sample_list[0]) is int
        assert type(sample_list[1]) is float
        assert type(sample_list[2]) is int
        assert type(sample_list[3]) is datetime
        assert type(sample_list[4]) is int
        assert type(sample_list[5]) is float

        data = json.dumps({
            'userid': sample_list[0],
            'floor_area': sample_list[1],
            'bedrooms': sample_list[2],
            'approval_date': datetime.strftime(sample_list[3], '%Y-%m-%d'),
            'lease_commencement_year': sample_list[4],
            'resale_pred': sample_list[5]
        })
        response = client.post('/api/prediction/add',
                               data=data,
                               content_type='application/json')

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        new_id = json.loads(response.get_data(as_text=True))["new_id"]

        assert new_id == sample_list[6]


@pytest.mark.xfail(reason='Null Entries')
@pytest.mark.parametrize('sample_list', [
    [None, 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0],
    [1, None, 3, datetime(1995, 10, 10), 1970, 100_000.0],
    [1, 100.0, None, datetime(1995, 10, 10), 1970, 100_000.0],
    [2, 55.5, 2, None, 1967, 67_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), None, 100_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, None]
])
def test_store_prediction_api_nulls(client, sample_list, capsys):
    test_store_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    ['1', 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0],
    [1, 'str', 3, datetime(1995, 10, 10), 1970, 100_000.0],
    [1, 100.0, '3', datetime(1995, 10, 10), 1970, 100_000.0],
    [2, 55.5, 2, 'date', 1967, 67_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), '1900', 100_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, '0.00']
])
def test_store_prediction_api_invalid(client, sample_list, capsys):
    test_store_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(reason='Entries Out of Range')
@pytest.mark.parametrize('sample_list', [
    [1, 0.0, 2, datetime(1990, 8, 8), 1967, 67_000.0],
    [1, 2000.0, 3, datetime(1995, 10, 10), 1970, 100_000.0],
    [1, 100.0, -1, datetime(1995, 10, 10), 1970, 100_000.0],
    [2, 55.5, 5, datetime(1800, 10, 10), 1967, 67_000.0],
    [1, 100.0, 3, datetime(2030, 10, 10), 1967, 100_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 1800, 100_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 2015, 100_000.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 0.0],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 2_000_000.0]
])
def test_store_prediction_api_out_of_range(client, sample_list, capsys):
    test_store_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


# Get latest prediction API
@pytest.mark.parametrize('sample_list', [
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3]
])
def test_get_latest_prediction_api(client, sample_list, capsys):
    with capsys.disabled():
        response = client.get(f'/api/prediction/get/latest/{sample_list[0]}')
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        pred = json.loads(response.get_data(as_text=True))

        assert pred['userid'] == sample_list[0]
        assert pred['floor_area'] == sample_list[1]
        assert pred['bedrooms'] == sample_list[2]
        assert pred['approval_date'] == datetime.strftime(
            sample_list[3], '%Y-%m-%d')
        assert pred['lease_commencement_year'] == sample_list[4]
        assert pred['resale_pred'] == sample_list[5]
        assert pred['id'] == sample_list[6]


@pytest.mark.xfail(reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    [2, 40.5, 2, datetime(1990, 8, 8), 1967, 67_000.0, 1],
    [2, 55.5, 1, datetime(1990, 8, 8), 1967, 67_000.0, 1],
    [2, 55.5, 2, datetime(1991, 8, 8), 1967, 67_000.0, 1],
    [2, 55.5, 2, datetime(1990, 8, 8), 1970, 67_000.0, 1],
    [2, 55.5, 2, datetime(1990, 8, 8), 1967, 101_000.0, 1],
    [2, 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0, 2],
    [1, 80.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3],
    [1, 100.0, 4, datetime(1995, 10, 10), 1970, 100_000.0, 3],
    [1, 100.0, 3, datetime(1996, 10, 10), 1970, 100_000.0, 3],
    [1, 100.0, 3, datetime(1995, 10, 10), 1971, 100_000.1, 3],
    [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 2]
])
def test_get_latest_prediction_api_invalid(client, sample_list, capsys):
    test_get_latest_prediction_api(client, sample_list, capsys)


# Get all predictions API
@pytest.mark.parametrize('sample_lists', [
    [
        [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3],
        [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 2]
    ],
    [
        [2, 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0, 1]
    ]
])
def test_get_all_predictions_api(client, sample_lists, capsys):
    with capsys.disabled():
        response = client.get(f'/api/prediction/get/{sample_lists[0][0]}')
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        predictions = json.loads(response.get_data(as_text=True))
        assert len(sample_lists) == len(predictions)

        for i in range(len(predictions)):
            pred = predictions[i]
            sample_list = sample_lists[i]
            assert pred['userid'] == sample_list[0]
            assert pred['floor_area'] == sample_list[1]
            assert pred['bedrooms'] == sample_list[2]
            assert pred['approval_date'] == datetime.strftime(
                sample_list[3], '%Y-%m-%d')
            assert pred['lease_commencement_year'] == sample_list[4]
            assert pred['resale_pred'] == sample_list[5]
            assert pred['id'] == sample_list[6]


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_lists', [
    [
        [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3],
        [1, 100.0, 3, datetime(1995, 10, 10), 1970, 200_000.0, 2]
    ],
    [
        [2, 55.5, 2, datetime(1990, 8, 8), 1967, 67_000.0, 2]
    ],
    [
        [0, 1]
    ]
])
def test_get_all_predictions_api_invalid(client, sample_lists, capsys):
    test_get_all_predictions_api(client, sample_lists, capsys)


# Delete prediction API
@pytest.mark.parametrize('sample_list', [
    1, 2
])
def test_remove_prediction_api(client, sample_list, capsys):
    with capsys.disabled():
        response = client.delete(f'/api/delete/{sample_list}')
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        result = json.loads(response.get_data(as_text=True))['result']
        assert result == 'ok'


@pytest.mark.xfail(reason='Record does not exist')
@pytest.mark.parametrize('sample_list', [
    10, 5
])
def test_remove_prediction_api_out_of_range(client, sample_list, capsys):
    test_remove_prediction_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.parametrize('sample_lists', [
    [
        [1, 100.0, 3, datetime(1995, 10, 10), 1970, 100_000.0, 3]
    ]
])
def test_get_all_predictions_api_after_deletion(client, sample_lists, capsys):
    test_get_all_predictions_api(
        client=client, sample_lists=sample_lists, capsys=capsys)
