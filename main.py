import requests, json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def find_unique_name(name, tier, language, enchant):
    # Load data from the JSON file

    item_tier = {"1": "Begginer's", "2": "Novie's", "3": "Journeymsn's", "4": "Adept's", "5": "Expert's", "6": "Master's", "7": "Grandmaster's", "8": "Elder's"}

    full_name = f"{item_tier[tier]} {name}"

    with open("./all_items.json", 'r', encoding='utf-8') as file:
        all_items = json.load(file)

    print(full_name)

    # Iterate through each item in the JSON data
    for item in all_items:
        # Check if the item has 'LocalizedNames' and if the English name matches
        if item.get('LocalizedNames') and item['LocalizedNames'].get(language) == full_name:
            if enchant == "0":
                return f"{item['UniqueName']}"
            else:
                return f"{item['UniqueName']}@{enchant}"

    # If the name is not found, return None
    return None

def searchitem(location, itemID, quality):
    url = f"https://west.albion-online-data.com/api/v2/stats/prices/{itemID}?locations={location}&qualities={quality}"

    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data")
        return None

@app.route('/<itemName>/<tier>/<enchants>/<location>', methods=['GET'])  
def get_items(itemName, tier, enchants, location):
    quality = request.args.get('quality', '')

    itemID = find_unique_name(itemName, tier, "EN-US", enchants);

    result = searchitem(location, itemID, quality)

    if result:
        return jsonify(result)
    else:
        return "Failed to retrieve data", 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
