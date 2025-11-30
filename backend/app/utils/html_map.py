import csv
from dataclasses import dataclass, field

import folium
from folium import MacroElement
from jinja2 import Template


@dataclass
class Location:
    """Represents a single location/place."""

    name: str
    latitude: float
    longitude: float
    category: str
    address: str = ""
    notes: str = ""
    zone: str = ""

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "Location":
        """Create a Location from a CSV row."""
        return cls(
            name=row.get("Name", "Unknown"),
            latitude=float(row.get("Latitude", 0)),
            longitude=float(row.get("Longitude", 0)),
            category=row.get("Category", "Other"),
            address=row.get("Address", ""),
            notes=row.get("Notes", ""),
            zone=row.get("Zone", ""),
        )


@dataclass
class Zone:
    """Represents a geographic zone with locations."""

    id: str
    name: str
    color: str
    center: list[float]
    zoom: int
    description: str
    polygon: list[list[float]] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)


@dataclass
class CountryConfig:
    """Configuration for a country's map."""

    center: list[float]
    zoom: int
    zones: list[Zone]


COUNTRY_CONFIGS: dict[str, CountryConfig] = {
    "Singapore": CountryConfig(
        center=[1.31, 103.84],
        zoom=12,
        zones=[
            Zone(
                id="chinatown",
                name="Chinatown & CBD",
                color="#e74c3c",
                center=[1.2820, 103.8440],
                zoom=16,
                description="Heritage shophouses, temples, and Michelin food.",
                polygon=[
                    [1.2885, 103.8430],
                    [1.2850, 103.8490],
                    [1.2780, 103.8470],
                    [1.2790, 103.8400],
                ],
            ),
            Zone(
                id="kampong",
                name="Kampong Glam & Bugis",
                color="#27ae60",
                center=[1.3010, 103.8580],
                zoom=16,
                description="Malay heritage, gin bars, and trendy lanes.",
                polygon=[
                    [1.3040, 103.8560],
                    [1.3030, 103.8620],
                    [1.2990, 103.8600],
                    [1.3000, 103.8550],
                ],
            ),
            Zone(
                id="civic",
                name="Civic District & Marina Bay",
                color="#2980b9",
                center=[1.2890, 103.8550],
                zoom=15,
                description="Museums, Skylines, and Supertrees.",
                polygon=[
                    [1.2980, 103.8480],
                    [1.2920, 103.8660],
                    [1.2780, 103.8660],
                    [1.2880, 103.8460],
                ],
            ),
            Zone(
                id="orchard",
                name="Orchard & Tanglin",
                color="#8e44ad",
                center=[1.3080, 103.8250],
                zoom=15,
                description="Shopping belt and lush gardens.",
                polygon=[
                    [1.3160, 103.8140],
                    [1.3050, 103.8400],
                    [1.2990, 103.8350],
                    [1.3100, 103.8100],
                ],
            ),
            Zone(
                id="east",
                name="Katong & East Coast",
                color="#d35400",
                center=[1.3080, 103.9000],
                zoom=15,
                description="Peranakan culture and laksa.",
                polygon=[
                    [1.3150, 103.9000],
                    [1.3140, 103.9080],
                    [1.3000, 103.9060],
                    [1.3000, 103.8950],
                ],
            ),
            Zone(
                id="outliers",
                name="Worth the Travel",
                color="#7f8c8d",
                center=[1.3500, 103.8000],
                zoom=11,
                description="Unique experiences further afield.",
            ),
        ],
    ),
    "Japan": CountryConfig(
        center=[35.68, 139.65],
        zoom=10,
        zones=[
            Zone(
                id="tokyo",
                name="Tokyo",
                color="#e74c3c",
                center=[35.68, 139.65],
                zoom=12,
                description="Capital city and urban exploration",
            ),
            Zone(
                id="osaka",
                name="Osaka",
                color="#27ae60",
                center=[34.67, 135.50],
                zoom=12,
                description="Street food and nightlife",
            ),
            Zone(
                id="kyoto",
                name="Kyoto",
                color="#2980b9",
                center=[35.01, 135.78],
                zoom=12,
                description="Temples, gardens, and tradition",
            ),
            Zone(
                id="other",
                name="Other Regions",
                color="#8e44ad",
                center=[35.5, 137.5],
                zoom=10,
                description="Day trips and regional explores",
            ),
        ],
    ),
    "Thailand": CountryConfig(
        center=[13.73, 100.52],
        zoom=10,
        zones=[
            Zone(
                id="bangkok",
                name="Bangkok",
                color="#e74c3c",
                center=[13.73, 100.52],
                zoom=12,
                description="Thailand's vibrant capital",
            ),
            Zone(
                id="north",
                name="Northern Thailand",
                color="#27ae60",
                center=[18.78, 98.98],
                zoom=10,
                description="Mountains and temples",
            ),
            Zone(
                id="south",
                name="Southern Beaches",
                color="#2980b9",
                center=[8.65, 100.14],
                zoom=10,
                description="Island paradise",
            ),
            Zone(
                id="central",
                name="Central Thailand",
                color="#d35400",
                center=[13.5, 99.5],
                zoom=10,
                description="Historical sites",
            ),
        ],
    ),
    "Vietnam": CountryConfig(
        center=[21.03, 105.85],
        zoom=9,
        zones=[
            Zone(
                id="hanoi",
                name="Hanoi",
                color="#e74c3c",
                center=[21.03, 105.85],
                zoom=12,
                description="Capital city charm",
            ),
            Zone(
                id="hcm",
                name="Ho Chi Minh City",
                color="#27ae60",
                center=[10.77, 106.70],
                zoom=12,
                description="Southern metropolis",
            ),
            Zone(
                id="danang",
                name="Da Nang",
                color="#2980b9",
                center=[16.07, 108.23],
                zoom=12,
                description="Beach city and Hoi An gateway",
            ),
            Zone(
                id="other",
                name="Other Regions",
                color="#8e44ad",
                center=[15.5, 107.0],
                zoom=9,
                description="Regional explores",
            ),
        ],
    ),
    "Malaysia": CountryConfig(
        center=[3.14, 101.69],
        zoom=10,
        zones=[
            Zone(
                id="kl",
                name="Kuala Lumpur",
                color="#e74c3c",
                center=[3.14, 101.69],
                zoom=12,
                description="Capital city exploration",
            ),
            Zone(
                id="penang",
                name="Penang",
                color="#27ae60",
                center=[5.41, 100.33],
                zoom=12,
                description="Heritage and beaches",
            ),
            Zone(
                id="malacca",
                name="Malacca",
                color="#2980b9",
                center=[2.20, 102.25],
                zoom=12,
                description="Historical port city",
            ),
            Zone(
                id="sabah",
                name="Sabah",
                color="#d35400",
                center=[5.37, 118.67],
                zoom=10,
                description="Borneo adventures",
            ),
        ],
    ),
}


def generate_html_map(
    csv_file: str, country: str = "Singapore", output_file: str | None = None
) -> None:
    from pathlib import Path

    if output_file is None:
        output_file = str(Path("output") / f"{country}_Planner_Desktop.html")

    # 1. Load Data from CSV
    locations: list[Location] = []
    try:
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader is None:
                print(f"Failed to read CSV file '{csv_file}'.")
                return
            for row in reader:
                locations.append(Location.from_csv_row(row))
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
        return

    if not locations:
        print(f"No locations found in '{csv_file}'.")
        return

    # 2. Get country configuration
    config = COUNTRY_CONFIGS.get(country, COUNTRY_CONFIGS["Singapore"])
    center = config.center
    zoom = config.zoom
    zones = config.zones

    # 3. Populate zones with locations from CSV
    for loc in locations:
        # Find matching zone by name
        zone_found = False
        for zone in zones:
            if zone.name.lower() == loc.zone.lower():
                zone.locations.append(loc)
                zone_found = True
                break

        # If no zone match found, assign to last zone (usually "Other/Worth the Travel")
        if not zone_found and zones:
            zones[-1].locations.append(loc)

    # 4. Create Map
    m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")

    # Helper for Icons
    def get_icon(cat: str) -> tuple[str, str]:
        cat = cat.lower()
        if "food" in cat or "sweet" in cat:
            return "red", "cutlery"
        if "bar" in cat:
            return "darkred", "glass"
        if "nature" in cat:
            return "green", "tree-deciduous"
        if "culture" in cat or "museum" in cat:
            return "orange", "star"
        if "unique" in cat:
            return "purple", "star"
        return "blue", "info-sign"

    # 5. Add Markers and Polygons
    marker_data: dict[str, dict[str, float | str]] = {}  # Store marker info for sidebar
    for zone in zones:
        # Add polygon for zone boundary
        if zone.polygon:
            folium.Polygon(
                locations=zone.polygon,
                color=zone.color,
                weight=2,
                fill=True,
                fill_color=zone.color,
                fill_opacity=0.4,
                tooltip=zone.name,
                popup=zone.description,
            ).add_to(m)

        # Add markers for locations
        for loc in zone.locations:
            try:
                color, icon = get_icon(loc.category)

                popup_html = f"""
                <div style="font-family:sans-serif; width:200px">
                    <b>{loc.name}</b><br>
                    <span style="color:gray; font-size:11px;">{loc.category}</span><hr>
                    {loc.notes}<br><br>
                    <small>📍 {loc.address}</small>
                </div>
                """

                marker = folium.Marker(
                    location=[loc.latitude, loc.longitude],
                    tooltip=loc.name,
                    popup=folium.Popup(popup_html, max_width=250),
                    icon=folium.Icon(color=color, icon=icon),
                )
                marker.add_to(m)

                # Store marker data for JavaScript access
                loc_key = f"{loc.name}_{loc.latitude}_{loc.longitude}"
                marker_data[loc_key] = {
                    "name": loc.name,
                    "lat": loc.latitude,
                    "lon": loc.longitude,
                }
            except (ValueError, KeyError):
                pass

    # 6. Sidebar Logic with Zoom-Based Opacity
    sidebar_html = """
    {% macro html(this, kwargs) %}
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <style>
        #map-sidebar {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 280px;
            max-height: 90vh;
            background-color: white;
            z-index: 9999;
            overflow-y: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border-radius: 8px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 10px;
        }
        .sidebar-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }
        .zone-container {
            margin-bottom: 8px;
            border: 1px solid #eee;
            border-radius: 5px;
            overflow: hidden;
        }
        .zone-title {
            padding: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            transition: all 0.3s ease;
        }
        .zone-title:hover {
            transform: translateX(2px);
            box-shadow: inset 0 -2px 4px rgba(0,0,0,0.1);
        }
        .location-list {
            display: none;
            padding: 5px 0;
            background-color: #fff;
        }
        .location-item {
            padding: 6px 15px;
            font-size: 13px;
            cursor: pointer;
            color: #555;
            border-left: 3px solid transparent;
        }
        .location-item:hover {
            background-color: #f0f8ff;
            color: #000;
            border-left: 3px solid #3498db;
        }
        .zone-dot {
            height: 10px;
            width: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        #map-sidebar::-webkit-scrollbar { width: 6px; }
        #map-sidebar::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
      </style>
    </head>
    <body>

    <div id="map-sidebar">
        <div class="sidebar-header">🌍 Trip Planner</div>

        {% for zone in this.zones %}
        <div class="zone-container" style="border-left: 4px solid {{ zone.color }};">
            <div class="zone-title" style="background: linear-gradient(90deg, {{ zone.color }}dd, {{ zone.color }}99);" onclick="flyToLoc({{ zone.center[0] }}, {{ zone.center[1] }}, {{ zone.zoom }}, '{{ zone.id }}')">
                <span><span class="zone-dot" style="background-color: white;"></span>{{ zone.name }} ({{ zone.locations|length }})</span>
                <span style="font-size:10px;">▼</span>
            </div>

            <div class="location-list" id="list-{{ zone.id }}">
                <div style="padding: 8px 15px; font-size: 12px; color: #666; font-style: italic;">{{ zone.description }}</div>
                {% for loc in zone.locations %}
                <div class="location-item" onclick="flyToLocAndOpen({{ loc.latitude }}, {{ loc.longitude }}, 18)">
                    📍 {{ loc.name }} <span style="font-size:10px; color:#aaa">({{ loc.category }})</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}

        <div style="font-size:11px; color:#999; margin-top:10px; text-align:center;">
            Click headers to zoom.<br>Click items to see pin.
        </div>
    </div>

    <script>
        var mapInstance = null;
        function findMap() {
            for (var key in window) {
                if (key.startsWith('map_') && window[key] && window[key].on) {
                    mapInstance = window[key];
                    initMapListeners();
                    break;
                }
            }
        }

        function flyToLocAndOpen(lat, lon, zoom) {
            if (!mapInstance) findMap();
            if (mapInstance) {
                mapInstance.flyTo([lat, lon], zoom, {
                    animate: true,
                    duration: 1.5
                });

                // Find and open the marker popup by coordinates
                setTimeout(function() {
                    mapInstance.eachLayer(function(layer) {
                        if (layer instanceof L.Marker) {
                            var markerLat = layer.getLatLng().lat;
                            var markerLon = layer.getLatLng().lng;
                            // Check if marker is at the target location (with small tolerance for floating point)
                            if (Math.abs(markerLat - lat) < 0.0001 && Math.abs(markerLon - lon) < 0.0001) {
                                layer.openPopup();
                            }
                        }
                    });
                }, 800);
            }
        }

        function flyToLoc(lat, lon, zoom, listId) {
            if (!mapInstance) findMap();
            if (mapInstance) {
                mapInstance.flyTo([lat, lon], zoom, {
                    animate: true,
                    duration: 1.5
                });

                if (listId) {
                    var list = document.getElementById("list-" + listId);
                    var allLists = document.getElementsByClassName("location-list");
                    for (var i=0; i<allLists.length; i++) {
                        if (allLists[i].id !== "list-" + listId) {
                            allLists[i].style.display = "none";
                        }
                    }
                    if (list.style.display === "block") {
                        list.style.display = "none";
                    } else {
                        list.style.display = "block";
                    }
                }
            }
        }

        function initMapListeners() {
            mapInstance.on('zoomend', function() {
                var zoom = mapInstance.getZoom();
                var newOpacity = (zoom >= 15) ? 0.1 : 0.45;
                mapInstance.eachLayer(function (layer) {
                    if (layer instanceof L.Polygon) {
                        layer.setStyle({fillOpacity: newOpacity});
                    }
                });
            });
            // Trigger once to set initial state
            var zoom = mapInstance.getZoom();
            var newOpacity = (zoom >= 15) ? 0.1 : 0.45;
            mapInstance.eachLayer(function (layer) {
                if (layer instanceof L.Polygon) {
                    layer.setStyle({fillOpacity: newOpacity});
                }
            });
        }

        findMap();
        setTimeout(findMap, 1000);
    </script>
    </body>
    </html>
    {% endmacro %}
    """

    class Sidebar(MacroElement):
        _template = Template(sidebar_html)

        def __init__(
            self, zones: list[Zone], marker_data: dict[str, dict[str, float | str]]
        ) -> None:
            super().__init__()
            self.zones = zones
            self.marker_data = marker_data

    m.get_root().add_child(Sidebar(zones, marker_data))
    m.save(output_file)
    print(f"✅ Desktop Map Generated: {output_file}")


if __name__ == "__main__":
    generate_html_map("singapore_places.csv", "Singapore")
