import pandas as pd
import folium
import webbrowser
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os
from data import ship_repo


ships_data = ship_repo.get_all_ships_tracking_details_from_db()
df = pd.DataFrame(ships_data)

print(df.head())

df['LAT'] = pd.to_numeric(df['LAT'])
df['LON'] = pd.to_numeric(df['LON'])
 
map_center = [df['LAT'].mean(), df['LON'].mean()]
ship_map = folium.Map(location=map_center, zoom_start=5)

for _, row in df.iterrows():
    popup_text = f"MMSI: {row['MMSI']}<br>VesselName: {row['VesselName']}<br>LAT: {row['LAT']}<br>LON: {row['LON']}"
    folium.Marker(
        location=[row['LAT'], row['LON']],
        popup=popup_text,
        icon=folium.Icon(icon="ship", prefix="fa")
    ).add_to(ship_map)

html_file = r'C:\Users\venti\Documents\Ship_tracking_project\ship_tracker_env\view\ship_map.html'
 
webbrowser.open(f'file:///{html_file}')

 
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Disable logging
 
os.chdir(os.path.dirname(html_file))
 
with TCPServer(("", 8000), Handler) as httpd:
    print("Serving at port 8000")
    httpd.serve_forever()

