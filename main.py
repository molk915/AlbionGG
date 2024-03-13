import requests, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def find_unique_name(name, tier, language, enchant):
    # Load data from the JSON file

    item_tier = {"1": "Begginer's", "2": "Novie's", "3": "Journeymsn's", "4": "Adept's", "5": "Expert's", "6": "Master's", "7": "Grandmaster's", "8": "Elder's"}

    full_name = f"{item_tier[tier]} {name}"

    with open("all_items.json", 'r', encoding='utf-8') as file:
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

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data")
        return None

def get_item_icons(itemID):
    url = f"https://render.albiononline.com/v1/item/{itemID}.png"

    response = requests.get(url)

    print(url)

    if response.status_code == 200:
        data = {f"{itemID}": url}
        with open("icon.json", "w") as json_file:
            json.dump(data, json_file)
        return data
    return None

def get_item_abilities(itemName):
    url = f"https://wiki.albiononline.com/wiki/{itemName}"

    
@app.route('/<itemName>/<tier>/<enchants>/<quality>/<location>', methods=['GET'])  
def get_items(itemName, tier, enchants, quality, location):

    itemID = find_unique_name(itemName, tier, "EN-US", enchants);

    result = searchitem(location, itemID, quality)

    if result:
        return jsonify(result, get_item_icons(itemID))
    else:
        return "Failed to retrieve data", 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
