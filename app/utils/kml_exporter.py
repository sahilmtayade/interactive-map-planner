import csv
import html


def create_kml(csv_file: str, country: str = "Singapore", output_file: str | None = None) -> None:
    """
    Generates a KML file that can be imported into Google My Maps.
    """
    from pathlib import Path

    if output_file is None:
        output_file = str(Path("output") / f"{country}_Trip_Mobile.kml")

    # KML Header
    kml_content: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        "<Document>",
        f"<name>{country} Trip Plan</name>",
        "<description>Generated from Python</description>",
    ]

    # Define Styles for Pins (Colors based on Category)
    styles: dict[str, str] = {
        "Food": "ff5252ff",  # Red
        "Sweet Tooth": "ff99ccff",  # Pink
        "Bar": "ff000099",  # Dark Red
        "Nature": "ff57bb8a",  # Green
        "Culture": "ffffcc33",  # Orange/Yellow
        "Unique": "ffba68c8",  # Purple
    }

    # Add Style Definitions to KML
    for cat, color in styles.items():
        kml_content.append(f'''
        <Style id="{cat.replace(" ", "_")}">
            <IconStyle>
                <color>{color}</color>
                <scale>1.1</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png</href>
                </Icon>
            </IconStyle>
        </Style>''')

    # Read CSV and create Placemarks
    try:
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader is None:
                print(f"Failed to read CSV file '{csv_file}'.")
                return
            for row in reader:
                name = html.escape(row["Name"])
                desc = html.escape(row["Notes"])
                address = html.escape(row["Address"])
                lat = row["Latitude"]
                lon = row["Longitude"]
                category = row["Category"]

                style_id = category.replace(" ", "_") if category in styles else "Unique"

                placemark = f"""
                <Placemark>
                    <name>{name}</name>
                    <description><![CDATA[<b>Category:</b> {category}<br><b>Address:</b> {address}<br><br>{desc}]]></description>
                    <styleUrl>#{style_id}</styleUrl>
                    <Point>
                        <coordinates>{lon},{lat},0</coordinates>
                    </Point>
                </Placemark>"""
                kml_content.append(placemark)

    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return

    # KML Footer
    kml_content.append("</Document></kml>")

    # Write file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(kml_content))

    print(f"✅ Mobile Map Generated: {output_file}")
    print("   -> Upload this file to https://www.google.com/mymaps to use on your phone.")


if __name__ == "__main__":
    create_kml("data/singapore_places.csv", "Singapore")
