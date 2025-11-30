import { useState } from "react";
import { api } from "../api/endpoints";
import type { Place } from "../types/schema";

interface SidebarProps {
  places: Place[];
  country: string;
  onPlaceAdded: () => void; // Callback to refresh data in parent
  onCountryChange: (c: string) => void;
}

export const Sidebar = ({
  places,
  country,
  onPlaceAdded,
  onCountryChange,
}: SidebarProps) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [category, setCategory] = useState("Food");
  const [loading, setLoading] = useState(false);

  const handleAdd = async () => {
    if (!searchQuery) return;
    setLoading(true);
    try {
      // 1. Search (calls Backend -> Nominatim)
      const result = await api.searchLocation(searchQuery, country);

      if (result.found) {
        // 2. Save to DB
        await api.addPlace({
          name: result.name,
          category: category,
          address: result.address,
          latitude: result.latitude,
          longitude: result.longitude,
          country: country,
          notes: "Added via Web App",
        });
        setSearchQuery("");
        onPlaceAdded(); // Refresh map
      } else {
        alert("Location not found!");
      }
    } catch (error) {
      console.error(error);
      alert("Error adding place");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sidebar">
      <h2 style={{ marginBottom: "20px" }}>✈️ Travel Planner</h2>

      {/* Country Selector */}
      <div className="control-group">
        <label>Destination:</label>
        <select
          value={country}
          onChange={(e) => onCountryChange(e.target.value)}
        >
          <option value="Singapore">Singapore</option>
          <option value="Japan">Japan</option>
          <option value="Malaysia">Malaysia</option>
        </select>
      </div>

      {/* Add New Place */}
      <div className="card add-box">
        <h3>➕ Add Place</h3>
        <input
          type="text"
          placeholder="Search e.g. Marina Bay"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="Food">Food</option>
          <option value="Bar">Bar</option>
          <option value="Nature">Nature</option>
          <option value="Culture">Culture</option>
        </select>
        <button onClick={handleAdd} disabled={loading}>
          {loading ? "Searching..." : "Search & Add"}
        </button>
      </div>

      {/* List */}
      <div className="list-container">
        <h3>📍 Itinerary ({places.length})</h3>
        <ul>
          {places.map((p) => (
            <li key={p.id} className="place-item">
              <span className={`tag ${p.category.toLowerCase()}`}></span>
              <div className="place-info">
                <strong>{p.name}</strong>
                <small>{p.category}</small>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
