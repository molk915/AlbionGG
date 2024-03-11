import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
function App() {
  const [tier, setTier] = useState("4");
  const [enchants, setEnchants] = useState("0");
  const [location, setLocation] = useState("");
  const [isVisible, setIsVisible] = useState(false);
  const getItems = async () => {
    const apiUrl = `http://localhost:5000/items/${tier}/${enchants}/${location}`;
    console.log("API URL:", apiUrl); // Wypisanie adresu URL na konsoli
    try {
      const { data } = await axios.get(apiUrl);
      console.log(data);
      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };

  return (
    <>
      <h1>Item Prices</h1>
      <select value={tier} onChange={(e) => setTier(e.target.value)}>
        <option value="4">Tier 4</option>
        <option value="5">Tier 5</option>
        <option value="6">Tier 6</option>
        <option value="7">tier 7</option>
        <option value="8">tier 8</option>
      </select>
      <select value={enchants} onChange={(e) => setEnchants(e.target.value)}>
        {" "}
        <option value="0">Enchants 0</option>
        <option value="1">Enchants 1</option>
        <option value="2">Enchants 2</option>
        <option value="3">Enchants 3</option>
        <option value="4">Enchants 4</option>
      </select>
      <select value={location} onChange={(e) => setLocation(e.target.value)}>
        <option value="Caerleon">Caerleon</option>
        <option value="Bridgewatch">Bridgewatch</option>
        <option value="Martlock">Martlock</option>
        <option value="Thetford">Thetford</option>
        <option value="FortSterling">Fort Sterling</option>
        <option value="Lymhurst">Lymhurst</option>
      </select>
      <button onClick={getItems}>Get Items</button>
    </>
  );
}

export default App;
