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

    if response.status_code == 200:
        data = url
        with open("icon.json", "w") as json_file:
            json.dump(data, json_file)
        return data
    return None

def get_item_abilities(itemName):
    session = requests.Session()
    url = f"https://wiki.albiononline.com/wiki/{itemName}"
    response = session.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', class_="wikitable")
        # Ignore the first table
        tables = tables[1:]
        abilities_list = []

        for i, table in enumerate(tables, 1):
            abilities_dict = {"slot": str(i), "abilities": {}}
            trs = table.find_all("tr")
            # Ignore first 3 rows of the table, but for the 5th table, ignore first 2 rows
            if i == 4:
                trs = trs[2:]
            else:
                trs = trs[3:]
            
            ability_index = 1  # Initialize ability index for each table
            for j, tr in enumerate(trs, 1):
                tds = tr.find_all("td", attrs={"rowspan": ["1", "2"]})
                for td in tds:
                    ability_text = td.text.strip()
                    if ability_text:
                        abilities_dict["abilities"][str(ability_index)] = ability_text
                        ability_index += 1

            abilities_list.append(abilities_dict)

        with open("abilities.json", "w") as json_file:
            json.dump(abilities_list, json_file, indent=4)

    else:
        print("Failed to fetch data from the URL:", url)

@app.route('/<itemName>/<tier>/<enchants>/<quality>/<location>', methods=['GET'])  
def get_items(itemName, tier, enchants, quality, location):

    itemID = find_unique_name(itemName, tier, "EN-US", enchants);

    result = searchitem(location, itemID, quality)

    get_item_abilities(itemName)

    if result:
        return jsonify(result, get_item_icons(itemID))
    else:
        return "Failed to retrieve data", 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)