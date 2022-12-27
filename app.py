from flask import Flask, jsonify, request
from hashlib import sha256
from json import load


app = Flask(__name__)
CONFIG_FILE_PATH = './config.json'
URL_HASH = ''
REQUESTS = []


with open(CONFIG_FILE_PATH) as config_file:
    sha256sum = sha256()
    config = load(config_file)
    sha256sum.update(bytes(config['plain_url'], 'utf-8'))
    URL_HASH = sha256sum.hexdigest()


@app.route("/get/<url_hash>")
def get_request(url_hash):
    if url_hash == URL_HASH and len(REQUESTS) > 0:
        return jsonify(REQUESTS.pop())
    else:
        return jsonify({})


@app.route("/put/<url_hash>")
def put_request(url_hash):
    if url_hash == URL_HASH:
        REQUESTS.append(request.args)
        return jsonify({'success': True})
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
