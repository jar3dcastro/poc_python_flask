from config import app
from flask import request, jsonify
#from werkzeug import datastructures
from os import listdir

# error handler
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

'''# make request mutable
@app.before_request
def before_request () :
    # change request object from InmutableMultiDict to MultiDict
    request.args = datastructures.MultiDict(request.args)'''

# import controllers
controllers = {}
files = [
    'TipoCambioController'
]
for file in files:
    module_name = file
    controller_name = module_name
    module = __import__('controllers.' + module_name, fromlist=[controller_name])
    controller = getattr(module, controller_name)
    controllers[controller_name] = controller
# routing base
def route (methods, uri, route_string) :
    # route string processing
    [controller, view_function_name] = route_string.split('@')
    view_func = getattr(controllers[controller], view_function_name)
    # methods processing
    if isinstance(methods, str):
        methods = [methods]
    methods = list(map(str.upper, methods))
    app.add_url_rule('/' + uri, view_func=view_func, methods=methods)

# routes
route('get',    'tipocambio/<fecha>',           'TipoCambioController@get_tipo_cambio')
