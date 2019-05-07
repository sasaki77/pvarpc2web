from threading import RLock

import pvaccess as pva
from .exception import InvalidRequest

from flask import current_app


class Pvaapi(object):
    """
    pvAccess api wrapper

    Attributes
    ----------
    timeout : float
        timeout for pvAccess RPC in seconds
    _clients : dict
        pvAccess RpcClient for ch name
    _lock : threading.RLock
        lock for _clients
    """

    def __init__(self, timeout=1):
        self.timeout = timeout
        self._clients = {}
        self._lock = RLock()

    def _get_rpc_client(self, ch_name):
        """Get pvAccess RPC Client

        Parameters
        ----------
        ch_name : str
            pvAccess channel name

        Returns
        -------
        pvaccess.RpcClient
            pvAccess RPC Client for channel name
        """
        self._check_ch_name(ch_name)
        name = str(ch_name)

        with self._lock:
            if name not in self._clients:
                self._clients[name] = pva.RpcClient(name)
            client = self._clients[name]

        return client

    def _create_request(self, params, path='', nturi=False):
        """Create pvAccess RPC request

        Parameters
        ----------
        params : dict
            parameters for optional RPC request query
        path : str
            path for nturi style path
        nturi : bool
            whether create request as nturi style or not

        Returns
        -------
        pvaccess.PvObject
            pvAccess RPC request pvData
        """

        query_type = {}
        query_val = {}

        for key, val in params.items():
            query_type[str(key)] = pva.STRING
            query_val[str(key)] = str(val)

        request = self._create_request_pvdata(query_type, query_val,
                                              path, nturi)

        return request

    def _create_request_pvdata(self, query_type, query_val, path='',
                               nturi=False):
        """Create RPC request pvData

        Parameters
        ----------
        query_type : dict
            dict of pvaccess type for query
        query_val : dict
            dict of query value
        path : str
            path for nturi style path
        nturi : bool
            whether create request as nturi style or not

        Returns
        -------
        pvaccess.PvObject
            pvAccess RPC request pvData
        """

        if nturi:
            request = pva.PvObject({'scheme': pva.STRING,
                                    'authority': pva.STRING,
                                    'path': pva.STRING,
                                    'query': query_type
                                    },
                                   'epics:nt/NTURI:1.0')
            request['scheme'] = 'pva'
            request['authority'] = ''
            request['path'] = str(path)
            request.setStructure('query', query_val)
        else:
            request = pva.PvObject(query_type)
            request.set(query_val)

        return request

    def _check_ch_name(self, ch_name):
        """Check RPC channel name is valid

        Parameters
        ----------
        ch_name : str or unicode
            channel name

        Raises
        ------
        InvalidRequest
            if channel name is invalid
        """

        if not ch_name:
            current_app.logger.error('valget: Empty ch name')
            raise InvalidRequest('RPC ch name is empty', status_code=400)

    def rpccall(self, ch_name, query, nturi=True):
        rpc = self._get_rpc_client(ch_name)

        request = self._create_request(query, ch_name, nturi)
        try:
            response = rpc.invoke(request, self.timeout)
        except pva.PvaException as e:
            raise InvalidRequest(str(e), status_code=400,
                                 details={'ch': ch_name})

        response.useNumPyArrays = False
        res = response.get()

        return res


pvaapi = Pvaapi()
