# test_main.py

from src.main import app
import pytest


@pytest.fixture
def client():
    return app.test_client()


# test /
def test_root(client):
    response = client.get('/')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# test the healthcheck
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'"healthy"' in response.data


# Test a normal recent date
def test_monthly_foobar_2023_11(client):
    response = client.get('/monthly_view_count/Foobar/2023/11')
    assert response.status_code == 200
    assert b'"14510"' in response.data


# Test another normal recent date
def test_monthly_foobar_2023_02(client):
    response = client.get('/monthly_view_count/Foobar/2023/02')
    assert response.status_code == 200
    assert b'"17887"' in response.data


# Test another normal recent date without zero padding on the month
def test_monthly_foobar_2023_2(client):
    response = client.get('/monthly_view_count/Foobar/2023/2')
    assert response.status_code == 200
    assert b'"17887"' in response.data


# Test a different article with a normal recent date
def test_monthly_kubernetes_2023_11(client):
    response = client.get('/monthly_view_count/Kubernetes/2023/11')
    assert response.status_code == 200
    assert b'"54066"' in response.data


# Test a date before Wikipedia existed
def test_monthly_foobar_1985_02(client):
    response = client.get('/monthly_view_count/Foobar/1985/02')
    assert response.status_code == 400
    assert b'"error"' in response.data


# Test missing year and month
def test_monthly_foobar(client):
    response = client.get('/monthly_view_count/Foobar')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# Test missing month
def test_monthly_foobar_2023(client):
    response = client.get('/monthly_view_count/Foobar/2023')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# Test a date in the very far future
# TODO: update this test before February 3000
def test_monthly_foobar_3000_02(client):
    response = client.get('/monthly_view_count/Foobar/3000/02')
    assert response.status_code == 400
    assert b'"error, queried date is in the future"' in response.data


# Test with an invalid month number (>12)
def test_monthly_foobar_2023_13(client):
    response = client.get('/monthly_view_count/Foobar/2023/13')
    assert response.status_code == 400
    assert b'"error, month must be an int between 1 and 12"' in response.data


# Test with an invalid month number (<1)
def test_monthly_foobar_2023_0(client):
    response = client.get('/monthly_view_count/Foobar/2023/0')
    assert response.status_code == 400
    assert b'"error, month must be an int between 1 and 12"' in response.data


# Test with 3 string params
def test_monthly_foobar_foobar_foobar(client):
    response = client.get('/monthly_view_count/Foobar/Foobar/Foobar')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# Test with 3 int params (where the "int" is a valid article)
def test_monthly_int_int_int(client):
    response = client.get('/monthly_view_count/2023/2023/11')
    assert response.status_code == 200
    assert b'"593627"' in response.data


# Test with string int string
def test_monthly_string_int_string(client):
    response = client.get('/monthly_view_count/Foobar/2023/Foobar')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# Test with string string int
def test_monthly_string_string_int(client):
    response = client.get('/monthly_view_count/Foobar/Foobar/11')
    assert response.status_code == 404
    assert b'Not Found' in response.data


# Test with too many params
def test_monthly_too_many_params(client):
    response = client.get('/monthly_view_count/Foobar/2023/11/11')
    assert response.status_code == 404
    assert b'Not Found' in response.data
