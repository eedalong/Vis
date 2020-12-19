# -*- coding: utf-8 -*-
#
import json
import logging
import time, timeit

import django
from django.http import HttpResponse, QueryDict
from django.views.generic import View

from codex.baseerror import BaseError, InputError


class BaseView(View):

    logger = logging.getLogger('View')

    def dispatch(self, request, *args, **kwargs):

        self.input = None
        self.request = request
        data = self.do_dispatch(*args, **kwargs)

        return data

    def do_dispatch(self, *args, **kwargs):
        raise NotImplementedError('You should implement do_dispatch() in sub-class of BaseView')

    def http_method_not_allowed(self, *args, **kwargs):
        return super(BaseView, self).http_method_not_allowed(self.request, *args, **kwargs)


class APIView(BaseView):

    logger = logging.getLogger('API')

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body or self.meta
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
        return self.api_wrapper(handler, *args, **kwargs)

    @property
    def body(self):
        return json.loads(self.request.body.decode() or '{}')

    @property
    def query(self):
        d = getattr(self.request, self.request.method, None)
        if d:
            d = d.dict()
        else:
            d = dict()
        d.update(self.request.FILES)
        return d

    @property
    def meta(self):
         d = QueryDict(self.request.META['QUERY_STRING'])
         return d.dict()

    def api_wrapper(self, func, *args, **kwargs):
        code = "SUCCESS"
        error_description = []
        result = None
        status = 200
        try:
            result = func(*args, **kwargs)
            if isinstance(result, django.http.response.HttpResponse):
                return result

        except BaseError as e:
            code = e.code
            error_description = e.error_description
            status = 599
            self.logger.exception('Error occurred when requesting %s: %s', self.request.path, e)

        except Exception as e:
            code = "INTERNAL_ERROR"
            error_description = [""]
            status = 500
            self.logger.exception('Error occurred when requesting %s: %s', self.request.path, e)

        try:
            response = json.dumps({
                'code': code,
                'error_description': error_description,
                'data': result,
            })
        except:
            self.logger.exception('JSON Serializing failed in requesting %s', self.request.path)
            code = 'INTERNAL_ERROR'
            error_description = ['服务器正在维修']
            status = 500
            response = json.dumps({
                'code': code,
                'error_description': error_description,
                'data': None,
            })
        return HttpResponse(response, content_type='application/json', status=status)

    def check_input(self, *keys):
        for k in keys:
            if k not in self.input:
                raise InputError('Field "%s" required' % (k, ))
