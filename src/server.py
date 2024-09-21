import sys
from json import dumps
from flask import Flask, request, make_response
from flask_cors import CORS
import matching

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


@APP.route("/match", methods=['POST'])
def match():
    '''/match route'''
    payload = request.get_json()

    # If there is no trade key in the payload
    if 'trade' not in payload:
        response = {
            "error": "Invalid Request",
            "message": "Trade name is missing"
        }
        return make_response(dumps(response), 400)
    
    # If there is no UOM key in the payload
    if 'unit_of_measure' not in payload:
        response = {
            "error": "Invalid Request",
            "message": "Unit of Measure is missing"
        }
        return make_response(dumps(response), 400)

    trade = payload['trade']
    unit_of_measure = payload['unit_of_measure']

    # Check if trade is an empty string and send appropriate error message
    if trade == '':
        response = {
            "error": "Invalid Request",
            "message": "Trade name cannot be empty"
        }
        return make_response(dumps(response), 400)
    
    # Check if UOM is an empty string and send appropriate error message
    if unit_of_measure == '':
        response = {
            "error": "Invalid Request",
            "message": "Unit of Measure name cannot be empty"
        }
        return make_response(dumps(response), 400)

    # Call match algorithm and get best match
    result = matching.bestMatch(trade, unit_of_measure)
    
    # If the best similarity score is below the threshold, then we say there is no match
    if result['similarity_score'] < 0.6:
        result['best_match'] = {
            "trade": "No Match",
            "unit_of_measure": "",
            "rate": 0
        }
        result['similarity_score'] = 0
        result['message'] = "No match found. Check the trade name for spellling errors. Use abbreviations for unit of measure with more than 4 letters and capitalize the abbreviations"
    
    return dumps(result)

if __name__ == "__main__":
    APP.run(port=6200, debug = True)
