import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def searchitem(location, itemname, tier, enchants, quality):
    url = f"https://west.albion-online-data.com/api/v2/stats/prices/T{tier}_{itemname}?locations={location}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data")
        return None

@app.route('/items/<tier>/<enchants>', methods=['GET'])  # Accepting tier as part of the URL
def get_items(tier, enchants):
    location = request.args.get('location', 'Caerleon,Bridgewatch')
    itemname = request.args.get('itemname', 'BAG')
    quality = request.args.get('quality', '')

    result = searchitem(location, itemname, tier, enchants, quality)
    if result:
        return jsonify(result)
    else:
        return "Failed to retrieve data", 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
