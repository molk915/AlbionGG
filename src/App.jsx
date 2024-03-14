import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [tier, setTier] = useState("4");
  const [enchants, setEnchants] = useState("0");
  const [location, setLocation] = useState("Bridgewatch");
  const [itemname, setItemName] = useState("Bag");
  const [quality, setQuality] = useState("1");
  const [itemData, setItemData] = useState(null);
  const [imageUrl, setImageUrl] = useState("");

  const getItems = async () => {
    const apiUrl = `http://localhost:5000/${itemname}/${tier}/${enchants}/${quality}/${location}`;
    try {
      const response = await axios.get(apiUrl);
      if (response.data && response.data.length > 0) {
        const itemInfo =
          response.data[0].length > 0 ? response.data[0][0] : null;
        if (itemInfo) {
          setItemData({
            sellPriceMax: itemInfo.sell_price_max,
            sellPriceMin: itemInfo.sell_price_min,
            buyPriceMax: itemInfo.buy_price_max,
            buyPriceMin: itemInfo.buy_price_min,
          });
        }
        if (response.data[1]) {
          setImageUrl(response.data[1]);
        }
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="App">
      <h1>Item Prices</h1>
      <input
        type="text"
        value={itemname}
        onChange={(e) => setItemName(e.target.value)}
        className="input-field"
      />
      <select
        value={tier}
        onChange={(e) => setTier(e.target.value)}
        className="select-box"
      >
        <option value="4">Tier 4</option>
        <option value="5">Tier 5</option>
        <option value="6">Tier 6</option>
        <option value="7">tier 7</option>
        <option value="8">tier 8</option>
      </select>
      <select
        value={enchants}
        onChange={(e) => setEnchants(e.target.value)}
        className="select-box"
      >
        <option value="0">Enchants 0</option>
        <option value="1">Enchants 1</option>
        <option value="2">Enchants 2</option>
        <option value="3">Enchants 3</option>
        <option value="4">Enchants 4</option>
      </select>
      <select
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        className="select-box"
      >
        <option value="Caerleon">Caerleon</option>
        <option value="Bridgewatch">Bridgewatch</option>
        <option value="Martlock">Martlock</option>
        <option value="Thetford">Thetford</option>
        <option value="FortSterling">Fort Sterling</option>
        <option value="Lymhurst">Lymhurst</option>
      </select>
      <select
        value={quality}
        onChange={(e) => setQuality(e.target.value)}
        className="select-box"
      >
        <option value="0">quality 1</option>
        <option value="1">quality 2</option>
        <option value="2">quality 3</option>
        <option value="3">quality 4</option>
        <option value="4">quality 5</option>
      </select>

      <button onClick={getItems} className="button">
        Get Items
      </button>

      {itemData && (
        <div>
          <p>Max Sell Price: {itemData.sellPriceMax}</p>
          <p>Min Sell Price: {itemData.sellPriceMin}</p>
          <p>Max Buy Price: {itemData.buyPriceMax}</p>
          <p>Min Buy Price: {itemData.buyPriceMin}</p>
        </div>
      )}
      {imageUrl && (
        <img
          src={imageUrl}
          alt="Item"
          style={{ maxWidth: "200px", maxHeight: "200px" }}
        />
      )}
    </div>
  );
}

export default App;
