import "leaflet/dist/leaflet.css";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import type { Place } from "../types/schema";

// Fix for default Leaflet marker icons in React
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface MapProps {
  places: Place[];
  center: [number, number];
  zoom: number;
}

export const MapView = ({ places, center, zoom }: MapProps) => {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />

      {places.map((place) => (
        <Marker
          key={place.id || Math.random()}
          position={[place.latitude, place.longitude]}
        >
          <Popup>
            <strong>{place.name}</strong>
            <br />
            <span style={{ color: "gray", fontSize: "0.9em" }}>
              {place.category}
            </span>
            <hr style={{ margin: "5px 0" }} />
            {place.notes}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};
