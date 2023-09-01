import open3d as o3d
import json
from geonav_conversions import xy2ll

def pcd_to_geojson(input_pcd, output_geojson, orglat, orglon):
    pcd = o3d.io.read_point_cloud(input_pcd)
    points = pcd.points
    coordinates = []
    for point in points:
        x, y, _ = point
        lon, lat = xy2ll(x, y, orglat, orglon)
        coordinates.append([lon, lat])

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "Name": "demo" 
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]
                },
                "id": 0
            }
        ]
    }

    with open(output_geojson, "w") as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2)

if __name__ == "__main__":
    input_pcd = "/home/vinusha/Documents/maps/pointcloud_map.pcd"  
    output_geojson = "output1.geojson"  
    orglat = 35.23808753540768  
    orglon = 139.9009591876285  

    pcd_to_geojson(input_pcd, output_geojson, orglat, orglon)

