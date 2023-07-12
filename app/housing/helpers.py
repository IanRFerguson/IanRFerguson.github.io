import folium
import pandas as pd
import json
import os

from app import here

##########

DATA_PATH = os.path.join(here, "static/housing/biography.json")
OUTPUT_PATH = os.path.join(here, "templates/housing")


def read_data_packet() -> dict:
    """Load JSON as dictionary"""

    with open(DATA_PATH) as incoming:
        return json.load(incoming)


def write_data_packet(data: dict) -> None:
    """Write dictionary to JSON"""

    with open(DATA_PATH, "w") as outgoing:
        json.dump(data, outgoing)


def build_map(key=None):
    """
    Read in data and write a local HTML file
    """

    # Read in data packet and render as dataframe
    data = read_data_packet()

    if key:
        data = data[key]
        location = [data["lon"], data["lat"]]
        zoom_start = 8
        output_name = f"map__{key}.html"

    else:
        location = [37.0902, -95.7129]
        zoom_start = 4
        output_name = "map__global.html"

    df = pd.DataFrame.from_dict(data, "index").reset_index(drop=False)

    ###

    g = folium.Map(location=location, zoom_start=zoom_start)

    for ix in df.index:
        lat = df["lat"][ix]
        lon = df["lon"][ix]
        address = f'<b>{df["address"][ix].upper()}</b>'

        folium.Marker(location=[lat, lon], popup=address).add_to(g)

    g.save(outfile=os.path.join(OUTPUT_PATH, output_name))


def get_rendered_map():
    pass


def isolate_values():
    pass
