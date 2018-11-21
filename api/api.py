from flask import Flask, request, jsonify, make_response, send_file
import json
import time

app = Flask(__name__)
app.config["DEBUG"] = True

file = '/Users/olujuwondare/PycharmProjects/untitled1/files/input.txt.json'


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route('/', methods=['GET'])
def home():
    return "<h1>Trips Endpoint Quickstart</h1>" \
           "<p>GET\t/api/v1/resources/records\t-->\tFetch all records" \
           "</p>" \
           "<p>POST\t/api/v1/resources/records/tripid\t-->\tCreate new trip record"


@app.route('/api/v1/resources/records', methods=['GET'])
def retrieve_all_entries():
    """
        Endpoint to retrieve all travel entries
        @:param => null
        @:returns => all entries from data source => GET
        @:returns => response code or error => DELETE
    """

    try:
        with open(file) as f:
            data = json.load(f)
            print(data)
    except OSError as err:
        print("File retrieval could not be completed : ", err)
        return
    return jsonify(data)


@app.route('/api/v1/resources/records', methods=['POST'])
def insert_entry():
    """
        Endpoint to insert new travel entry
        @:param => null
        @:returns => all entries from data source => GET
        @:returns => response code or error => DELETE
    """
    content = request.get_json()

    def lastindex(data):
        return max(node['primaryid'] for node in data)

    try:
        with open(file) as f:
            data = json.load(f)
            content['primaryid'] = lastindex(data) + 1
            data.append(content)
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
        return "200"
    except OSError as err:
        raise InvalidUsage('Illegal request', status_code=410)


@app.route('/api/v1/resources/records', methods=['DELETE'])
def delete_entry():
    """
        Endpoint to delete existing travel entry
        @:param => null
        @:returns => all entries from data source => GET
        @:returns => response code or error => DELETE
    """
    content = request.get_json()
    try:
        with open(file) as f:
            data = json.load(f)
    except OSError as err:
        print(err)
    if content not in data:
        return jsonify({"data":"No such content to delete"})
    else:
        for a in range(0, len(data)):
            if content == data[a]:
                data.pop(a)
                break
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
        return "200"


@app.route('/api/v1/resources/records/<int:id>', methods=['PUT'])
def update_entry(id):
    """
        Endpoint to update a specific travel entries
        @:param => JSON Object with fields (datetime, description, elevation, id, latitutde, longitude)
    """

    try:
        with open(file) as f:
            data = json.load(f)
            i = [i for i in data if i['primaryid'] == id]
            if len(i) == 0:
                return not_found(404)
            if not request.json:
                return abort(400)
            if len(request.json['elevation']) == 0:
                return abort(400)
            if len(request.json['description']) == 0:
                return abort(400)
            if len(request.json['longitude']) == 0:
                return abort(400)
            if len(request.json['latitude']) == 0:
                return abort(400)

            i[0]['datetime'] = request.json.get('datetime', i[0]['datetime'])
            i[0]['description'] = request.json.get('description', i[0]['description'])
            i[0]['elevation'] = request.json.get('elevation', i[0]['elevation'])
            i[0]['latitude'] = request.json.get('latitude', i[0]['latitude'])
            i[0]['longitude'] = request.json.get('longitude', i[0]['longitude'])
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
        return jsonify({'status': 'success'})
    except BaseException:
        raise InvalidUsage('Error occured - Cannot update', status_code=410)


@app.route('/api/v1/resources/records/docxfile')
def downloadDocxFile ():
    """
        Endpoint for converting and downloading current object to .docx file
        :return: .docx file
    """
    converter.convert_to_docx(file)
    time.sleep(5)
    f = '/Users/olujuwondare/PycharmProjects/untitled1/files/input.txt.docx'
    return send_file(f, as_attachment=True, attachment_filename='updated_input.txt.docx')


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def abort():
    return make_response(jsonify({'error': 'Empty value provided'}), 400)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.run()