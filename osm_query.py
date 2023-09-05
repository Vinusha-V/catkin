import overpy
import geopandas as gpd
from shapely.geometry import LineString, Point
import yaml

# Read configuration from YAML file
def read_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load configuration from your YAML file
config_file = "varma_clean_map_config.yaml"
config = read_config(config_file)

# Define the latitude and longitude coordinates from the configuration
latitude = config.get('latitude', 0.0)  # Replace with your key from YAML
longitude = config.get('longitude', 0.0)  # Replace with your key from YAML

# Create a Point geometry from the coordinates
point = Point(longitude, latitude)

# Define the search radius (50 km)
search_radius_km = 50

# Convert the search radius to degrees (approximately)
# 1 degree of latitude is about 111 km
# 1 degree of longitude varies based on latitude, but we'll approximate it as 111 km for this example
degrees_per_km = 1 / 111  # Approximation
search_radius_degrees = search_radius_km * degrees_per_km

# Calculate bounding box coordinates
min_lon = longitude - search_radius_degrees
max_lon = longitude + search_radius_degrees
min_lat = latitude - search_radius_degrees
max_lat = latitude + search_radius_degrees

# Create an Overpass API instance
api = overpy.Overpass()

# Construct the Overpass QL query to search for highways within the bounding box
query = f"""
[out:json];
(
  way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
);
out body;
>;
out skel qt;
"""

# Send the query to the Overpass API
result = api.query(query)

# Create a list to store LineString geometries
geometries = []

for way in result.ways:
    coords = [(node.lon, node.lat) for node in way.nodes]
    line = LineString(coords)
    geometries.append(line)

# Create a GeoDataFrame from the LineString geometries
gdf = gpd.GeoDataFrame(geometry=geometries)

# Save the GeoDataFrame as a shapefile
gdf.to_file("output.shp")
