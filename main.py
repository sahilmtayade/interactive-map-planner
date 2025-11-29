from pathlib import Path

from utils import create_kml, generate_html_map


def find_countries():
    """Discover countries by looking for folders with a 'data' subfolder."""
    countries = {}
    current_dir = Path.cwd()

    for item in sorted(current_dir.iterdir()):
        if item.is_dir() and (item / "data").exists():
            country_name = item.name.capitalize()
            countries[str(len(countries) + 1)] = {
                "name": country_name,
                "path": item,
            }

    return countries


def get_country_choice():
    """Prompt user to select a country."""
    countries = find_countries()

    if not countries:
        print("Error: No country folders with 'data' subfolder found.")
        print(
            "Please ensure you have folders like 'singapore/', 'japan/', etc. with 'data/' subfolders."
        )
        return None

    print("\n--- Trip Builder ---")
    print("\nSelect a country:")
    for key, country in countries.items():
        print(f"{key}. {country['name']}")

    choice = input(f"\nEnter your choice (1-{len(countries)}): ").strip()

    if choice in countries:
        return countries[choice]["name"], countries[choice]["path"]
    else:
        print("Invalid choice. Defaulting to the first option.")
        first_country = countries["1"]
        return first_country["name"], first_country["path"]


def main():
    result = get_country_choice()
    if not result:
        return

    country_name, country_path = result

    # Find the CSV file in the data subfolder
    data_folder = country_path / "data"
    csv_files = list(data_folder.glob("*_places.csv"))

    if not csv_files:
        print(f"Error: No '*_places.csv' file found in {data_folder}")
        return

    csv_file = str(csv_files[0])
    print(f"\n1. Reading '{csv_file}'...")

    # Setup output folder
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    # Generate KML file for Google My Maps
    kml_output = str(output_folder / f"{country_name}_Trip_Mobile.kml")
    create_kml(csv_file, country_name, kml_output)

    # Generate single HTML file for Desktop Planning
    html_output = str(output_folder / f"{country_name}_Planner.html")
    generate_html_map(csv_file, country_name, html_output)

    print("\n" + "=" * 60)
    print("✨ Files generated in 'output' folder!")
    print(f"🌏 Open 'output/{country_name}_Planner.html' in your browser")
    print(f"📍 Or import 'output/{country_name}_Trip_Mobile.kml' to Google My Maps")
    print("=" * 60)


if __name__ == "__main__":
    main()
