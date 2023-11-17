import pytest

from app import app
from service import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_create_new_form(client):
    data = {
        'form_name': 'Test NewForm',
        'order_date': '2023-11-17',
        'phone_number': '+7 913 892 55 90',
        'lead_email': 'test@mail.com',
        'text_message': 'This test message'
    }
    resp = client.post('/create_form', data=data)
    assert resp.status_code == 200
    assert 'result_validate' in resp.json 
    assert 'result_insert' in resp.json
    assert resp.json['result_insert'] == 'success'


def test_create_new_form_not_validate_field(client):
    data = {
        'form_name': 'Test NewForm',
        'order_date': '2023-11-1',
        'phone_number': '+7 913 892 55 90',
        'lead_email': 'test@mail.com',
        'text_message': 'This test message'
    }
    resp = client.post('/create_form', data=data)
    assert resp.status_code == 400
    assert 'result_validate' in resp.json
    assert 'result_insert' not in resp.json


def test_get_form(client):
    data = {
        'form_name': 'Test NewForm',
        'order_date': '2023-11-17',
        'phone_number': '+7 913 892 55 90',
        'lead_email': 'test@mail.com',
        'text_message': 'This test message'
    }
    resp = client.post('/get_form', data=data)
    assert resp.status_code == 200
    assert 'search_form_result' in resp.json 
    assert resp.json['search_form_result'] == 'Test NewForm'


def test_get_form_not_found(client):
    data = {
        'order_date': '2018-11-17',
        'lead_email': 'tGTHDD@mail.com',
        'phone_number': '+7 111 222 55 90',
        'text_message': 'This test message'
    }
    resp = client.post('/get_form', data=data)
    assert resp.status_code == 400
    assert 'search_form_result' in resp.json
    assert type(resp.json['search_form_result']) == dict


def test_get_form_not_validate_field(client):
    data = {
        'order_date': '2023-11-1',
        'phone_number': '+7 913 892 55 90',
        'lead_email': 'test@mail.com',
        'text_message': 'This test message'
    }
    resp = client.post('/get_form', data=data)
    assert resp.status_code == 400
    assert 'search_form_result' in resp.json
    assert type(resp.json['search_form_result']) == dict