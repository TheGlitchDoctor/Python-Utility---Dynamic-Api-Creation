from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from functions_lookup import functions_lookup
import inspect
import ast
import sys


app1=Flask(__name__)

#route='/dynamic/'+str(sys.argv[2])
#@app1.route(route, methods=['GET', 'POST'])
#def func_router_endpoint(func_name=str(sys.argv[2])):
@app1.route('/dynamic/<func_name>', methods=['GET', 'POST'])
def func_router_endpoint(func_name):
    if func_name in functions_lookup.keys():
        data = []

        func_inspect = inspect.getfullargspec(functions_lookup[func_name])
        if len(func_inspect[0]) != 0:  # if func has required params
            data_dict = eval(request.data)
            # Check if those params are given by the user
            for key in func_inspect[0]:
                if key not in data_dict.keys():  # if param missing, return error with required params
                    return jsonify({'result': 'unknown', 'reason': "%s parameters required! Some are missing!" % (",".join(func_inspect[0]))}), 404
                else:
                    data.append(data_dict[key])

            # if func has no args or kwargs
            if func_inspect[1] == None and func_inspect[2] == None:
                return jsonify({'result': functions_lookup[func_name](*data)}), 200

            elif func_inspect[1] == 'args':  # if func also has args dynamic params
                for key in sorted(data_dict.keys()):  # append those params to data
                    if data_dict[key] not in data:
                        data.append(data_dict[key])
                return jsonify({'result': functions_lookup[func_name](*data)}), 200

            elif func_inspect[2] == 'kwargs':  # if func also has kwargs dynamic params
                data_kwargs = eval(request.data)
                for key, val in data_kwargs.items():  # filter extra data from request to a new dictionary
                    if val in data:
                        del data_kwargs[key]
                return jsonify({'result': functions_lookup[func_name](*data, **data_kwargs)}), 200

        # if func has no defined parameters and only dynamic params
        elif len(func_inspect[0]) == 0:
            data_dict = eval(request.data)
            if func_inspect[1] == 'args':  # if func has dynamic params args
                for key in sorted(data_dict.keys()):
                    data.append(data_dict[key])
                return jsonify({'result': functions_lookup[func_name](*data)}), 200

            elif func_inspect[2] == 'kwargs':  # if func has dynamic params kwargs
                return jsonify({'result': functions_lookup[func_name](**data_dict)}), 200

    else:
        return jsonify({'result': 'unknown', 'reason': 'invalid function name provided'}), 404


app1.run(host='127.0.0.1', port=str(sys.argv[1]))