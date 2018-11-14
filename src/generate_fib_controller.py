#! /usr/bin/env python

from flask import Flask
from flask.globals import request
from flask import jsonify
from flask.helpers import make_response

from http import HTTPStatus

import os
import json
import datetime
import timeit
import psutil

import fib_model
import generate_fib_service

import logging
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)

from mongoengine import *
connect('fib', host='store', port=27017)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def it_works():
    return 'It Works'


@app.route("/fib/<string:start_idx>/<string:end_idx>", methods=['GET'])
def get_fibonacci_numbers(start_idx, end_idx):
   
    try:
        data_to_be_stored = {}
        data_to_be_stored['request_log_time'] = datetime.datetime.utcnow 
        data_to_be_stored['request'] = str(request) 
               
        if request.method == 'GET':
            start_idx = int(start_idx)
            end_idx = int(end_idx)
        else:
            LOGGER.error('%s - This HTTP method is not supported. Please use and HTTP GET' %(request.method) )
            return make_response(json.dumps({'error': 'HTTP ' + request.method + ' is not supported, please use an HTTP GET'}), HTTPStatus.METHOD_NOT_ALLOWED)
        
        if start_idx < 0 or end_idx <0 :
            LOGGER.error('The "start_idx/end_idx" parameter can not be a negative number')
            resp = make_response(json.dumps({'error': 'The "start_idx/end_idx" parameter can not be a negative number'}), HTTPStatus.INTERNAL_SERVER_ERROR)
  
        elif (end_idx < start_idx):
            LOGGER.error('The "end_idx" parameter can not be less than start index')
            resp = make_response(json.dumps({'error': 'The "end_idx" parameter can not be less than start index'}), HTTPStatus.INTERNAL_SERVER_ERROR)

        elif (end_idx-start_idx) < 1:
            LOGGER.error('start_idx and end_idx cannot be same')
            resp = make_response(json.dumps({'error': 'start_idx and end_idx cannot be same'}), HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            try:
                #LOGGER.info(timeit.timeit(generate_fib_service.gen_fib_index_range_cache(start_idx, end_idx)))
                fib_num_dict = generate_fib_service.gen_fib_index_range_cache(start_idx, end_idx)
                resp = make_response(json.dumps(fib_num_dict), HTTPStatus.CREATED)
            except Exception as err:
                LOGGER.info(err.__str__())
            
        LOGGER.info('Fibonacci numbers are successfully created')
        LOGGER.info(json.loads(resp.data))
        data_to_be_stored['response'] = json.loads(resp.data)
        data_to_be_stored['status_code'] = resp.status_code

        try:
            model = fib_model.RequestLog(**data_to_be_stored)
            create = model.save()
        except Exception as err:
            LOGGER.info(err.__str__())
        return resp
    except Exception as err:
            LOGGER.info(err.__str__()) 

@app.route("/health", methods=['GET'])
def get_status():
    LOGGER.info('/heath has been called')
    try:
        memory_used_in_percentage = psutil.virtual_memory().percent
        LOGGER.info(memory_used_in_percentage)
        if memory_used_in_percentage > 90:
            return make_response(json.dumps({'status' : 'Memory usage has crossed 90%'})), HTTPStatus.OK

        return make_response(json.dumps({'status': 'Everything is perfect'})), HTTPStatus.OK
    except Exception as err:
        LOGGER.info(err.__str__())

if __name__ == '__main__':

    PORT = int(os.environ.get("FIB_PORT", 32001))
    app.run(debug=False, host='0.0.0.0', port=PORT)
