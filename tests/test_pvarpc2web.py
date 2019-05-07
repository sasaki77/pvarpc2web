import pytest

from .context import pvarpc2web


@pytest.fixture
def query():
    return {
             'ch_name': 'ET_SASAKI:PVARPC2WEB:TEST:add_nturi',
             'query': {
                 'lhs': 1,
                 'rhs': 1
                 },
            }


def test_get_method_request_with_nturi(client, query):
    ch = query['ch_name']
    lhs = query['query']['lhs']
    rhs = query['query']['rhs']
    rv = client.get('/?ch_name={}&lhs={}&rhs={}'.format(ch, lhs, rhs))
    json_data = rv.get_json()
    assert json_data['value'] == 2


def test_get_method_request_without_nturi(client, query):
    ch = 'ET_SASAKI:PVARPC2WEB:TEST:add'
    lhs = query['query']['lhs']
    rhs = query['query']['rhs']
    rv = client.get('/?ch_name={}&lhs={}&rhs={}&nonturi'.format(ch, lhs, rhs))
    json_data = rv.get_json()
    assert json_data['value'] == 2


def test_get_method_request_without_chname(client, query):
    lhs = query['query']['lhs']
    rhs = query['query']['rhs']
    rv = client.get('/?lhs={}&rhs={}'.format(lhs, rhs))
    json_data = rv.get_json()
    res = {'message': 'Invalid query'}
    res['details'] = {'request': None}
    assert rv.status_code == 400
    assert json_data == res


def test_query_add_without_nturi(client, query):
    query['nturi'] = False
    query['ch_name'] = 'ET_SASAKI:PVARPC2WEB:TEST:add'
    rv = client.post('/', json=query)
    json_data = rv.get_json()
    assert json_data['value'] == 2


def test_query_add_with_nturi(client, query):
    rv = client.post('/', json=query)
    json_data = rv.get_json()
    assert json_data['value'] == 2


def test_query_invalid_query_type(client, query):
    del query['ch_name']
    rv = client.post('/', json=query)
    json_data = rv.get_json()
    res = {'message': 'Invalid query'}
    res['details'] = {'request': query}
    assert rv.status_code == 400
    assert json_data == res


def test_query_empyt_ch(client, query):
    query['ch_name'] = ''
    rv = client.post('/', json=query)
    json_data = rv.get_json()
    res = {'message': 'RPC ch name is empty'}
    res['details'] = {}
    assert rv.status_code == 400
    assert json_data == res


def test_query_not_exist_ch(client, query):
    query['ch_name'] = 'NOT:EXIST:CH'
    rv = client.post('/', json=query)
    json_data = rv.get_json()
    res = {'message': 'connection timeout'}
    res['details'] = {'ch': 'NOT:EXIST:CH'}
    assert rv.status_code == 400
    assert json_data == res
