# -*- coding: utf-8 -*-

# The MIT License
#
# Copyright (c) 2010 Juhani Åhman <juhani.ahman@cs.helsinki.fi>
# Copyright (c) 2013 Flowroute LLC <matthew@flowroute.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
'''
调用的格式为
{
"func":"login",
"para": {"mac":"c8:ee:a6:03:20:a6","hostname":"CN-WLMQ-2001-22","tqisfull":0}
}

返回值的格式自定义，可能是json，也可能是文本
'''

import types
import json

from twisted.application import service
from twisted.internet import defer, reactor
from twisted.python import log

DEFAULT_JSONRPC = '0.0.1'

class JSONRPCService(object):
    """
    The JSONRPCService class is a JSON-RPC
    """

    def __init__(self, timeout=None, reactor=reactor):
        self.method_data = {}
        self.serve_exception = None
        self.out_of_service_deferred = None
        self.pending = set()
        self.timeout = timeout
        self.reactor = reactor

    def add(self, f, name=None, types=None, required=None):
        """
        Adds a new method to the jsonrpc service.

        Arguments:
        f -- the remote function
        name -- name of the method in the jsonrpc service
        types -- list or dictionary of the types of accepted arguments
        required -- list of required keyword arguments

        If name argument is not given, function's own name will be used.

        Argument types must be a list if positional arguments are used or a
        dictionary if keyword arguments are used in the method in question.

        Argument required MUST be used only for methods requiring keyword
        arguments, not for methods accepting positional arguments.
        """
        if name is None:
            fname = f.__name__  # Register the function using its own name.
        else:
            fname = name

        self.method_data[fname] = {'method': f}

        if types is not None:
            self.method_data[fname]['types'] = types

            if required is not None:
                self.method_data[fname]['required'] = required

    def stopServing(self, exception=None):
        """
        Returns a deferred that will fire immediately if there are
        no pending requests, otherwise when the last request is removed
        from self.pending.
        """
        if exception is None:
            exception = ServiceUnavailableError
        self.serve_exception = exception
        if self.pending:
            d = self.out_of_service_deferred = defer.Deferred()
            return d
        return defer.succeed(None)

    def startServing(self):
        self.serve_exception = None
        self.out_of_service_deferred = None

    def cancelPending(self):
        pending = self.pending.copy()
        for i in pending:
            i.cancel()

    @defer.inlineCallbacks
    def call(self, jsondata, protocal):
        result = yield self.call_py(jsondata, protocal)
        if result is None:
            defer.returnValue(None)
        else:
            defer.returnValue(json.dumps(result))

    @defer.inlineCallbacks
    def call_py(self, jsondata, protocal):
        try:
            try:
                rdata = json.loads(jsondata, strict=False)
            except Exception as e:
                try:
                    rdata = eval(jsondata)
                except Exception as e:
                    raise ParseError
        except ParseError, e:
            defer.returnValue(self._get_err(e))
            return

        try:
            if isinstance(rdata, dict) and rdata:
                rdata.update({"rpcconn": protocal})
                respond = yield self._handle_request(rdata)
                if respond is None:
                    defer.returnValue(None)
                else:
                    defer.returnValue(respond)
                return
            else:
                # empty dict, list or wrong type
                raise InvalidRequestError
        except InvalidRequestError, e:
            defer.returnValue(self._get_err(e))
        except Exception, e:
            defer.returnValue(self._get_err(e))

    def _get_err(self, e, id=None, jsonrpc=DEFAULT_JSONRPC):
        """
        Returns jsonrpc error message.
        """
        # Do not respond to notifications when the request is valid.
        if not id \
                and not isinstance(e, ParseError) \
                and not isinstance(e, InvalidRequestError):
            return None

        respond = {}
        respond['error'] = e.dumps()
        return respond


    @defer.inlineCallbacks
    def _call_method(self, request):
        """Calls given method with given params and returns it value."""
        method = self.method_data[request['func']]['method']
        rpcconn = request["rpcconn"]
        params = request['para']
        params["rpcconn"] = rpcconn
        result = None

        try:
            if isinstance(params, dict):
                result = yield defer.maybeDeferred(method, **params)
        except Exception:
            # Exception was raised inside the method.
            log.msg('Exception raised while invoking RPC method "{}".'.format(
                    request['method']))
            log.err()
            raise ServerError

        defer.returnValue(result)

    def _remove_pending(self, d):
        self.pending.remove(d)
        if self.out_of_service_deferred and not self.pending:
            self.out_of_service_deferred.callback(None)

    @defer.inlineCallbacks
    def _handle_request(self, request):
        """Handles given request and returns its response."""
        if self.serve_exception:
            raise self.serve_exception()

        d = self._call_method(request)

        self.pending.add(d)
        if self.timeout:
            timeout_deferred = self.reactor.callLater(self.timeout, d.cancel)

            def completed(result):
                if timeout_deferred.active():
                    # cancel the timeout_deferred if it has not been fired yet
                    # this is to prevent d's deferred chain from firing twice
                    # (and raising an exception).
                    timeout_deferred.cancel()
                return result
            d.addBoth(completed)
        try:
            result = yield d
        except defer.CancelledError:
            # The request was cancelled due to a timeout or by cancelPending
            # having been called. We return a TimeoutError to the client.
            self._remove_pending(d)
            raise TimeoutError()
        except Exception as e:
            self._remove_pending(d)
            raise e
        self._remove_pending(d)
        defer.returnValue(result)


class ServiceStopped(Exception):
    """
    A request was made of a stopped JSONRPCClientService.
    """
    pass


class JSONRPCError(Exception):
    """
    JSONRPCError class based on the JSON-RPC 2.0 specs.

    code - number
    message - string
    data - object
    """
    code = 0
    message = None
    data = None

    def __init__(self, message=None):
        """Setup the Exception and overwrite the default message."""
        if message is not None:
            self.message = message

    def dumps(self):
        """Return the Exception data in a format for JSON-RPC."""

        error = {'code': self.code,
                 'message': str(self.message)}

        if self.data is not None:
            error['data'] = self.data

        return error

#==============================================================================
# Exceptions
#
# The error-codes -32768 .. -32000 (inclusive) are reserved for pre-defined
# errors.
#
# Any error-code within this range not defined explicitly below is reserved
# for future use
#==============================================================================

class ParseError(JSONRPCError):
    """Invalid JSON. An error occurred on the server while parsing the JSON
    text."""
    code = -32700
    message = 'Parse error'


class InvalidRequestError(JSONRPCError):
    """The received JSON is not a valid JSON-RPC Request."""
    code = -32600
    message = 'Invalid request'


class MethodNotFoundError(JSONRPCError):
    """The requested remote-procedure does not exist / is not available."""
    code = -32601
    message = 'Method not found'


class InvalidParamsError(JSONRPCError):
    """Invalid method parameters."""
    code = -32602
    message = 'Invalid params'

    def __init__(self, data=None):
        self.data = data


class InternalError(JSONRPCError):
    """Internal JSON-RPC error."""
    code = -32603
    message = 'Internal error'


# -32099..-32000 Server error. Reserved for implementation-defined
# server-errors.
class KeywordError(JSONRPCError):
    """The received JSON-RPC request is trying to use keyword arguments even
    tough its version is 1.0."""
    code = -32099
    message = 'Keyword argument error'


class TimeoutError(JSONRPCError):
    """The request took too long to process."""
    code = -32098
    message = 'Server Timeout'


class ServiceUnavailableError(JSONRPCError):
    """The service is not available (stopServing called)."""
    code = -32097
    message = 'Service Unavailable'


class ServerError(JSONRPCError):
    """Generic server error."""
    code = -32000
    message = 'Server error'
