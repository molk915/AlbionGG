import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [tier, setTier] = useState("4");
  const [enchants, setEnchants] = useState("0"); // State for enchantments

  const getItems = async () => {
    const { data } = await axios.get(
      `http://localhost:5000/items/${tier}/${enchants}` // Adjusted URL to include enchants
    );
    console.log(data);
    return data;
  };

  return (
    <>
      <h1>Item Prices</h1>
      <select value={tier} onChange={(e) => setTier(e.target.value)}>
        <option value="4">Tier 4</option>
        <option value="5">Tier 5</option>
        <option value="6">Tier 6</option>
        {/* Add more options for other tiers */}
      </select>
      <select value={enchants} onChange={(e) => setEnchants(e.target.value)}>
        {" "}
        {/* Added onchange event to update enchant state */}
        <option value="0">Enchants 0</option>
        <option value="1">Enchants 1</option>
        <option value="2">Enchants 2</option>
        <option value="3">Enchants 3</option>
        <option value="4">Enchants 4</option>
      </select>
      <button onClick={getItems}>Get Items</button>
    </>
  );
}

export default App;
