# from flask import Flask, jsonify, make_response, request as flask_request
# from ner_tag import NER
# app = Flask(__name__)

# if __name__ == '__main_':
#     app.run(debug=True, port=5000) #run app in debug mode on port 5000
from flask import Flask, url_for, jsonify, make_response, request as flask_request
from ner_tag import NER
app = Flask(__name__)
ner = NER()
@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/api/v1/real-estate-extraction', methods=['POST'])
def sense_v1():
    """This is a legacy API, we will maintain it until all requests are moved to
    V2."""
    global ner
    texts = flask_request
    if not flask_request.is_json:
        raise ValueError('Expecting a json request')
    reqs = flask_request.get_json()
    if not isinstance(reqs, list):
        reqs = [reqs]
    print(reqs)
    results = ner.predict(reqs)
    return make_response(jsonify(results), 200)
