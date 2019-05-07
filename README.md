# pvarpc2web - http / pvAccess API gateway

This package is API gateway for pvAccess RPC server.

It receives http requests and return data from pvAccess RPC server.

## Installing

```bash
# clone the repository
git clone https://github.com/sasaki77/pvarpc2web
cd pvarpc2web
# install pvarpc2web
pip install -e .
```

## Usage

Simple usage is below.
```bash
export FLASK_APP=pvarpc2web
export FLASK_ENV=development
export PVARPC2WEB_CONFIG=/absolute/path/to/config/file
flask run --port=3003
```

See [here](http://flask.pocoo.org/) for more flask information.

## Configuration

Refer config file example [pvarpc2web.cfg](https://github.com/sasaki77/pvarpc2web/blob/master/pvarpc2web.cfg).

## HTTP Methods
### Get request

`ch_name` must be requiered for a get request.
The other parameters are optional.

`nonturi` parameter is used for a pure pvAccess RPC service.

```
http://?ch_name=chname&nonturi=0&param1=param1&param2=param2
```

### Post request
A Post request sholud use `application/json`.
The body of message must include `ch_name` and the others are optional.

`nturi` determines a request argument style. If `nturi` is not 0 or `nturi` is not in the post request, the request argument is sent as NTURI.

```
{
  "ch_name": "ch_name"
  "nturi": 0
  "query": { "myParam": "someValue", ... }
}
```


## Test

Install packages for develop
```bash
pip install -e .[develop]
```

Before runnging tests, test pvAccess RPC server must be running.

```bash
python tests/pvaserver/run.py
```

Run without coverage:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov pvarpc2web
coverage report -m
```
