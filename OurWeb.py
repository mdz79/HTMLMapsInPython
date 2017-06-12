'''
Smal script for creation of the map of our real-estate.
Index.html will be created with all real-estate.
Each real-estate will have separate .html, based on name in specification file.

You have to add arguments in following order ... host login password

Example:
python3 OurWeb.py AnyWeb.com user psswd

'''
import folium
import pandas as pd
from unidecode import unidecode
import glob  # module for listing of file with given extension
import pysftp # SFTP module for direct upload to web
import sys # module to read arguments from command line

RealE_df = pd.read_csv("RE_List.csv") # Specification of the source file

# Transformation of DataFrame to lists ...
lat = list(RealE_df["Latitude"])
lon = list(RealE_df["Lontitude"])
City = list(RealE_df["Miesto"])
REType = list(RealE_df["Druh"])

# Color switch function fro marker

def Color_Marker(inp_x):
    if inp_x == "Obchody":
        return "green"
    elif inp_x == "Reštaurácia/Bar":
        return "blue"
    elif inp_x == "Výroba/Sklady":
        return "red"
    elif inp_x == "Pozemok":
        return "orange"
    else:
        return "black"

def MyIcon(inp_x):
    if inp_x == "Obchody":
        return "shopping-cart"
    elif inp_x == "Reštaurácia/Bar":
        return "glass"
    elif inp_x == "Výroba/Sklady":
        return "cog"
    elif inp_x == "Pozemok":
        return "tree-deciduous"
    else:
        return "ok"


# Definition of Main Map

map = folium.Map(location=[48.531057, 17.248993], zoom_start=10) # Main map and the level of zoom

reg = folium.FeatureGroup(name="Naša mapa")

for lt,ln,ct,ty in zip(lat,lon,City,REType): # creation of markers
    reg.add_child(folium.Marker(location=[lt,ln],popup=(ct+", "+ty), icon=folium.Icon(color=Color_Marker(ty), icon=MyIcon(ty))))

map.add_child(reg)
map.save("index.html") #Save whole map with all markers

# Definition of Smaller maps (Single entity map)

for  lt,ln,ct,ty in zip(lat,lon,City,REType):
    map2 = folium.Map(location=[lt,ln], zoom_start=15)  # Small map fo each property
    newName = unidecode((ct+"-"+ty[:4])).lower() #creates new file name based on city and type of property
    reg2 = folium.FeatureGroup(name=("Mapa"+ct))
    reg2.add_child(folium.Marker(location=[lt,ln],popup=(ct+", "+ty), icon=folium.Icon(color=Color_Marker(ty), icon=MyIcon(ty))))
    map2.add_child(reg2)
    map2.save((newName+".html")) # creates new file awith required name

#Check what files do we have in pwd
List_of_Files = glob.glob("*.html")

#Send all file to Server / SFTP
cnopts = pysftp.CnOpts() # avoiding host key ... if none is provided
cnopts.hostkeys = None

#connect to server via SFTP and save files there ...
try:
    Secure_Con = pysftp.Connection(sys.argv[1], username=sys.argv[2], password=sys.argv[3], cnopts=cnopts )
    #sys.argv[1] = host, sys.argv[2] = username, sys.argv[3]= password
    for file1 in List_of_Files:
        Secure_Con.put(file1)

    Secure_Con.close()
except OSError:
    print('cannot open', arg)
