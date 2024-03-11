import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def searchitem(location, itemname, tier, enchants, quality):
    url = f"https://west.albion-online-data.com/api/v2/stats/prices/T{tier}_{itemname}@{enchants}?locations={location}&qualities={quality}" if enchants != "0" else f"https://west.albion-online-data.com/api/v2/stats/prices/T{tier}_{itemname}?locations={location}&qualities={quality}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data")
        return None

@app.route('/items/<tier>/<enchants>/<location>', methods=['GET'])  
def get_items(tier, enchants, location):
    itemname = request.args.get('itemname', 'BAG')
    quality = request.args.get('quality', '')

    result = searchitem(location, itemname, tier, enchants, quality)
    if result:
        return jsonify(result)
    else:
        return "Failed to retrieve data", 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
