# 🇸🇬 Interactive Singapore Trip Planner

A full-stack data application designed to simplify group travel planning. It replaces spreadsheets with an interactive map interface, utilizing **OpenStreetMap** for free geocoding and **Streamlit** for real-time data editing.

## 🚀 Features

- **Interactive Mapping:** Visualize itinerary points using Folium & Leaflet.
- **Live Data Editing:** Edit notes, categories, and itineraries in an Excel-like interface (Pandas + Streamlit).
- **Smart Search:** Integrated Nominatim (OSM) API to find and pinpoint locations without Google API keys.
- **Mobile Sync:** Auto-generates KML files to sync itineraries with Google Maps Mobile.
- **Strict Engineering:** Built with 100% type safety (`mypy`) and PEP-8 compliance (`ruff`).

## 🛠️ Tech Stack

- **Core:** Python 3.11+
- **Framework:** Streamlit
- **Geospatial:** Folium, Geopy, OpenStreetMap
- **Data:** Pandas
- **Tooling:** `uv` (Package Management), `ruff` (Linting), `mypy` (Typing)

## 📦 How to Run

This project uses **uv** for blazing fast dependency management.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/sahilmtayade/interactive-map-planner.git
    cd interactive-map-planner
    ```

2.  **Run the application:**
    ```bash
    uv run streamlit run app.py
    ```

## 🧪 Development

To ensure code quality, use pre-commit or run the static analysis tools:

```bash
uv run pre-commit install
```

```bash
# Type Checking
uv run mypy .

# Linting
uv run ruff check .
```
