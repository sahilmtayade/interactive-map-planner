import { useEffect, useState } from "react";
import { api } from "./api/endpoints";
import "./App.css";
import { MapView } from "./components/MapView";
import { Sidebar } from "./components/Sidebar";
import type { Place } from "./types/schema";

// Config centers for maps
const CENTERS: Record<string, [number, number]> = {
  Singapore: [1.3521, 103.8198],
  Japan: [36.2048, 138.2529],
  Malaysia: [4.2105, 101.9758],
};

function App() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [country, setCountry] = useState("Singapore");

  const refreshData = () => {
    api.getPlaces(country).then(setPlaces);
  };

  // Load data on mount or country change
  useEffect(() => {
    refreshData();
  }, [country]);

  return (
    <div className="app-container">
      <Sidebar
        places={places}
        country={country}
        onCountryChange={setCountry}
        onPlaceAdded={refreshData}
      />
      <div className="map-wrapper">
        <MapView
          places={places}
          center={CENTERS[country] || [0, 0]}
          zoom={country === "Singapore" ? 11 : 6}
        />
      </div>
    </div>
  );
}

export default App;
