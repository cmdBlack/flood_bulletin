"""
Description: A script to automate generation of Daily Hydrological Forecast
             for Abra River Basin located in Northern Luzon Philippines.
            
AUTHOR: KAIZER MACNI

"""

import os
import warnings
import sys
import re
warnings.filterwarnings("ignore")
from pathlib import Path

from qgis.core import *
from PyQt5.QtWidgets import QApplication
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from qgis.PyQt.QtGui import (
    QPolygonF,
    QColor,
)

from qgis.PyQt.QtCore import (
    QPointF,
    QRectF,
    QSize,
)

from qgis.PyQt.QtXml import QDomDocument


from datetime import date
os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"

#FUNCTION DECLARATIONS
def x_stat_color(stat,color):
    if stat == "NORMAL":
        color.setSymbol(NORMAL)
    elif stat == "ALERT":
        color.setSymbol(ALERT)
    elif stat == "ALARM":
        color.setSymbol(ALARM)
    elif stat == "CRITICAL":
        color.setSymbol(CRITICAL)
    else:
        color.setSymbol(NORMAL)

#import warnings
#warnings.filterwarnings("ignore")

#VARIABLES

#RISING
#RECEDING
#NSC

#wl_buntun = "NSC"
#wl_tumauini = "NSC"
#wl_gamu = "NSC"

#wl_pared = "NSC"
#wl_penablanca = "NSC"
#wl_tabuk = "NSC"
#wl_angadanan = "NSC"
#wl_pangal = "NSC"
#wl_nagtipunan = "NSC"
#wl_piat = "NSC"

with open("input1.txt", "r") as file1:
    content1 = file1.readlines()
    print(content1)
    
with open("input2.txt", "r") as file2:
    content2 = file2.readlines()
    print(content2)

"""
# input tstm string
print("Enter WL status and affected municipalities")
lines = sys.stdin.readlines()
print(lines)
status = "".join(lines) # Join the list of lines back into a single string
#print("\n--- Your input ---")
#print(status)
#print(lines[0])
"""

for line in content1:
    if "BUNTUN" in line:
        buntun_line = line.strip("\n").split("-")
        wl_buntun_stat = buntun_line[1]
        wl_buntun = buntun_line[2]
    elif "TUMAUINI" in line:
        tumauini_line = line.strip("\n").split("-")
        wl_tumauini_stat = tumauini_line[1]
        wl_tumauini = tumauini_line[2]
    elif "GAMU" in line:
        gamu_line = line.strip("\n").split("-")
        wl_gamu_stat = gamu_line[1]
        wl_gamu = gamu_line[2]
    elif "PARED" in line:
        pared_line = line.strip("\n").split("-")
        wl_pared_stat = pared_line[1]
        wl_pared = pared_line[2]
    elif "PENABLANCA" in line:
        penablanca_line = line.strip("\n").split("-")
        wl_penablanca_stat = penablanca_line[1]
        wl_penablanca = penablanca_line[2]
    elif "TABUK" in line:
        tabuk_line = line.strip("\n").split("-")
        wl_tabuk_stat = tabuk_line[1]
        wl_tabuk = tabuk_line[2]
    elif "ANGADANAN" in line:
        angadanan_line = line.strip("\n").split("-")
        wl_angadanan_stat = angadanan_line[1]
        wl_angadanan = angadanan_line[2]
    elif "PANGAL" in line:
        pangal_line = line.strip("\n").split("-")
        wl_pangal_stat = pangal_line[1]
        wl_pangal = pangal_line[2]
    elif "NAGTIPUNAN" in line:
        nagtipunan_line = line.strip("\n").split("-")
        wl_nagtipunan_stat = nagtipunan_line[1]
        wl_nagtipunan = nagtipunan_line[2]
        print(wl_nagtipunan)
    elif "PIAT" in line:
        piat_line = line.strip("\n").split("-")
        wl_piat_stat = piat_line[1]
        wl_piat = piat_line[2]
        print(wl_piat)
    else:
        pass

for line in content1:
    if "possible" in line:
        yellow_mun = line.split("possible[")[1].split("]")[0].split(",")
        yellow_mun = [mun.lower() for mun in yellow_mun]
        print(yellow_mun)
    elif "threatening" in line:
        orange_mun = line.split("threatening[")[1].split("]")[0].split(",")
        orange_mun = [mun.lower() for mun in orange_mun]
        print(orange_mun)
    elif "occur" in line:
        red_mun = line.split("occur[")[1].split("]")[0].split(",")
        red_mun = [mun.lower() for mun in red_mun]
        print(red_mun)
    elif "persisting" in line:
        purple_mun = line.split("persisting[")[1].split("]")[0].split(",")
        purple_mun = [mun.lower() for mun in purple_mun]
        print(purple_mun)
    else:
        pass

###########################################################


app = QApplication([])
#qgs.setPrefixPath("C:\\OSGeo4W\\apps\\qgis-ltr", True)
QgsApplication.setPrefixPath("C:\\OSGeo4W\\apps\\qgis-ltr", True)
qgs = QgsApplication([], False)

qgs.initQgis()

canvas = QgsMapCanvas()

project = QgsProject.instance()
bridge = QgsLayerTreeMapCanvasBridge(project.layerTreeRoot(), canvas)
#project.read("D:\\DAILY REPORT\\WL change monitoring\\000abraBasinREPORTHF_automated.qgz")

current_dir = Path.cwd()

# Create the directory and any missing parent directories
os.makedirs(str(current_dir) + "\\out\\png", exist_ok=True)
os.makedirs(str(current_dir) + "\\out\\svg", exist_ok=True)
os.makedirs(str(current_dir) + "\\out\\pdf", exist_ok=True)

os.makedirs(str(current_dir) + "\\out2\\png", exist_ok=True)
os.makedirs(str(current_dir) + "\\out2\\svg", exist_ok=True)
os.makedirs(str(current_dir) + "\\out2\\pdf", exist_ok=True)


print(str(current_dir) + "\\CRB_bulletin.qgz")

#project.read("C:\\Users\\kjjma\\OneDrive\\Desktop\\project\\cagayanriverbasin_fb\\CRB_bulletin.qgz")
project.read(str(current_dir) + "\\CRB_bulletin.qgz")

layer = project.mapLayersByName('CRBV')[0]

features = layer.getFeatures()
for feature in features:
    # Access feature attributes
    mun_name = feature.attribute('NAME_2')
    if isinstance(mun_name, str):
        mun_name = mun_name.lower()
    flood_cat = feature.attribute('flood_cat')

    with edit(layer):
        if mun_name in purple_mun:
            feature['flood_cat'] = 4        
        elif mun_name in red_mun:
            feature['flood_cat'] = 3
        elif mun_name in orange_mun:
            feature['flood_cat'] = 2
        elif mun_name in yellow_mun:
            feature['flood_cat'] = 1
        else:
            feature['flood_cat'] = 0


        layer.updateFeature(feature)
        up_flood = feature.attribute('flood_cat')



today = date.today()
#today = "2024-10-03"


project = QgsProject.instance()
            
manager = project.layoutManager()
layouts_list = manager.printLayouts()




layout = QgsPrintLayout(project)
layout.initializeDefaults()

        
document = QDomDocument()

# read template content
#template_file = open("C:\\Users\\kjjma\\OneDrive\\Desktop\\project\\cagayanriverbasin_fb\\crb_template.qpt")
template_file = open(str(current_dir) + "\\crb_template.qpt")

template_content = template_file.read()
template_file.close()
document.setContent(template_content)


# load layout from template and add to Layout Manager
layout.loadFromTemplate(document, QgsReadWriteContext()) 
project.layoutManager().addLayout(layout)


BELOW_ALERT = QgsFillSymbol.createSimple({'color': 'white'})
NORMAL = QgsFillSymbol.createSimple({'color': 'green'})
ALERT = QgsFillSymbol.createSimple({'color': 'yellow'})
ALARM = QgsFillSymbol.createSimple({'color': 'orange'})
CRITICAL = QgsFillSymbol.createSimple({'color': 'red'})

####  WATER LEVEL  #####################

#wl_pared = "NSC"
#wl_penablanca = "NSC"
#wl_tabuk = "NSC"
#wl_angadanan = "NSC"
#wl_pangal = "NSC"
#wl_nagtipunan = "NSC"
#wl_piat = "NSC"

BUNTUN_WL_STAT = wl_buntun + "_BUNTUN"
TUMAUINI_WL_STAT = wl_tumauini + "_TUMAUINI"
GAMU_WL_STAT = wl_gamu + "_GAMU"

PARED_WL_STAT = wl_pared + "_PARED"
PENABLANCA_WL_STAT = wl_penablanca + "_PENABLANCA"
TABUK_WL_STAT = wl_tabuk + "_TABUK"
ANGADANAN_WL_STAT = wl_angadanan + "_ANGADANAN"
PANGAL_WL_STAT = wl_pangal + "_PANGAL"
NAGTIPUNAN_WL_STAT = wl_nagtipunan + "_NAGTIPUNAN"
PIAT_WL_STAT = wl_piat + "_PIAT"

layout = QgsProject.instance().layoutManager().layoutByName("cagayan")

#waterlevels
buntun_wl_img_status = layout.itemById(BUNTUN_WL_STAT)
buntun_wl_img_status.setVisibility(1)
tumauini_wl_img_status = layout.itemById(TUMAUINI_WL_STAT)
tumauini_wl_img_status.setVisibility(1)
gamu_wl_img_status = layout.itemById(GAMU_WL_STAT)
gamu_wl_img_status.setVisibility(1)
pared_wl_img_status = layout.itemById(PARED_WL_STAT)
pared_wl_img_status.setVisibility(1)
penablanca_wl_img_status = layout.itemById(PENABLANCA_WL_STAT)
penablanca_wl_img_status.setVisibility(1)
tabuk_wl_img_status = layout.itemById(TABUK_WL_STAT)
tabuk_wl_img_status.setVisibility(1)
angadanan_wl_img_status = layout.itemById(ANGADANAN_WL_STAT)
angadanan_wl_img_status.setVisibility(1)
pangal_wl_img_status = layout.itemById(PANGAL_WL_STAT)
pangal_wl_img_status.setVisibility(1)
nagtipunan_wl_img_status = layout.itemById(NAGTIPUNAN_WL_STAT)
nagtipunan_wl_img_status.setVisibility(1)
piat_wl_img_status = layout.itemById(PIAT_WL_STAT)
piat_wl_img_status.setVisibility(1)



"""    
#BUNTUN ALERT=4.6, ALARM=6.8, CRITICAL=9.0
wl_buntun_val = float(wl_buntun_stat)
if wl_buntun_val < 4.6:
    buntun_wl_img_status.setSymbol(NORMAL)
elif 4.6 <= wl_buntun_val < 6.8:
    buntun_wl_img_status.setSymbol(ALERT)
elif 6.8 <= wl_buntun_val < 9.0:
    buntun_wl_img_status.setSymbol(ALARM)
elif wl_buntun_val >= 9.0:
    buntun_wl_img_status.setSymbol(CRITICAL)
"""

x_stat_color(wl_buntun_stat,buntun_wl_img_status)
x_stat_color(wl_tumauini_stat,tumauini_wl_img_status)
x_stat_color(wl_gamu_stat,gamu_wl_img_status)
x_stat_color(wl_pared_stat,pared_wl_img_status)
x_stat_color(wl_penablanca_stat,penablanca_wl_img_status)
x_stat_color(wl_tabuk_stat,tabuk_wl_img_status)
x_stat_color(wl_angadanan_stat,angadanan_wl_img_status)
x_stat_color(wl_pangal_stat,pangal_wl_img_status)
x_stat_color(wl_tabuk_stat,tabuk_wl_img_status)
x_stat_color(wl_nagtipunan_stat,nagtipunan_wl_img_status)
x_stat_color(wl_piat_stat,piat_wl_img_status)




"""
if wl_buntun_stat == "NORMAL":
    buntun_wl_img_status.setSymbol(NORMAL)
elif wl_buntun_stat == "ALERT":
    buntun_wl_img_status.setSymbol(ALERT)
elif wl_buntun_stat == "ALARM":
    buntun_wl_img_status.setSymbol(ALARM)
elif wl_buntun_stat == "CRITICAL":
    buntun_wl_img_status.setSymbol(CRITICAL)
else:
    buntun_wl_img_status.setSymbol(NORMAL)
    


tumauini_wl_img_status = layout.itemById(TUMAUINI_WL_STAT)
tumauini_wl_img_status.setVisibility(1)



if wl_tumauini_stat == "NORMAL":
    tumauini_wl_img_status.setSymbol(NORMAL)
elif wl_tumauini_stat == "ALERT":
    tumauini_wl_img_status.setSymbol(ALERT)
elif wl_tumauini_stat == "ALARM":
    tumauini_wl_img_status.setSymbol(ALARM)
elif wl_tumauini_stat == "CRITICAL":
    tumauini_wl_img_status.setSymbol(CRITICAL)
else:
    tumauini_wl_img_status.setSymbol(NORMAL)

gamu_wl_img_status = layout.itemById(GAMU_WL_STAT)
gamu_wl_img_status.setVisibility(1)
"""
"""
#GAMU ALERT=3.9, ALARM=7.7, CRITICAL=11.3
wl_gamu_val = float(wl_gamu_stat)
if wl_gamu_val < 3.9:
    gamu_wl_img_status.setSymbol(NORMAL)
elif 3.9 <= wl_gamu_val < 7.7:
    gamu_wl_img_status.setSymbol(ALERT)
elif 7.7  <= wl_gamu_val < 11.3:
    gamu_wl_img_status.setSymbol(ALARM)
elif wl_gamu_val >= 11.3:
    gamu_wl_img_status.setSymbol(CRITICAL)
"""
"""
if wl_gamu_stat == "NORMAL":
    gamu_wl_img_status.setSymbol(NORMAL)
elif wl_gamu_stat == "ALERT":
    gamu_wl_img_status.setSymbol(ALERT)
elif wl_gamu_stat == "ALARM":
    gamu_wl_img_status.setSymbol(ALARM)
elif wl_gamu_stat == "CRITICAL":
    gamu_wl_img_status.setSymbol(CRITICAL)
else:
    gamu_wl_img_status.setSymbol(NORMAL)
    

#wl_pared = "NSC"
#wl_penablanca = "NSC"
#wl_tabuk = "NSC"
#wl_angadanan = "NSC"
#wl_pangal = "NSC"
#wl_nagtipunan = "NSC"
#wl_piat = "NSC"

pared_wl_img_status = layout.itemById(PARED_WL_STAT)
pared_wl_img_status.setVisibility(1)

if wl_pared_stat == "NORMAL":
    pared_wl_img_status.setSymbol(NORMAL)
elif wl_tumauini_stat == "ALERT":
    pared_wl_img_status.setSymbol(ALERT)
elif wl_tumauini_stat == "ALARM":
    pared_wl_img_status.setSymbol(ALARM)
elif wl_tumauini_stat == "CRITICAL":
    pared_wl_img_status.setSymbol(CRITICAL)
else:
    pared_wl_img_status.setSymbol(NORMAL)

penablanca_wl_img_status = layout.itemById(PENABLANCA_WL_STAT)
penablanca_wl_img_status.setVisibility(1)

if wl_penablanca_stat == "NORMAL":
    penablanca_wl_img_status.setSymbol(NORMAL)
elif wl_penablanca_stat == "ALERT":
    penablanca_wl_img_status.setSymbol(ALERT)
elif wl_penablanca_stat == "ALARM":
    penablanca_wl_img_status.setSymbol(ALARM)
elif wl_penablanca_stat == "CRITICAL":
    penablanca_wl_img_status.setSymbol(CRITICAL)
else:
    penablanca_wl_img_status.setSymbol(NORMAL)

tabuk_wl_img_status = layout.itemById(TABUK_WL_STAT)
tabuk_wl_img_status.setVisibility(1)

if wl_tabuk_stat == "NORMAL":
    tabuk_wl_img_status.setSymbol(NORMAL)
elif wl_tabuk_stat == "ALERT":
    tabuk_wl_img_status.setSymbol(ALERT)
elif wl_tabuk_stat == "ALARM":
    tabuk_wl_img_status.setSymbol(ALARM)
elif wl_tabuk_stat == "CRITICAL":
    tabuk_wl_img_status.setSymbol(CRITICAL)
else:
    tabuk_wl_img_status.setSymbol(NORMAL)

angadanan_wl_img_status = layout.itemById(ANGADANAN_WL_STAT)
angadanan_wl_img_status.setVisibility(1)

if wl_angadanan_stat == "NORMAL":
    angadanan_wl_img_status.setSymbol(NORMAL)
elif wl_angadanan_stat == "ALERT":
    angadanan_wl_img_status.setSymbol(ALERT)
elif wl_angadanan_stat == "ALARM":
    angadanan_wl_img_status.setSymbol(ALARM)
elif wl_angadanan_stat == "CRITICAL":
    angadanan_wl_img_status.setSymbol(CRITICAL)
else:
    angadanan_wl_img_status.setSymbol(NORMAL)

pangal_wl_img_status = layout.itemById(PANGAL_WL_STAT)
pangal_wl_img_status.setVisibility(1)

if wl_pangal_stat == "NORMAL":
    pangal_wl_img_status.setSymbol(NORMAL)
elif wl_pangal_stat == "ALERT":
    pangal_wl_img_status.setSymbol(ALERT)
elif wl_pangal_stat == "ALARM":
    pangal_wl_img_status.setSymbol(ALARM)
elif wl_pangal_stat == "CRITICAL":
    pangal_wl_img_status.setSymbol(CRITICAL)
else:
    pangal_wl_img_status.setSymbol(NORMAL)

nagtipunan_wl_img_status = layout.itemById(NAGTIPUNAN_WL_STAT)
nagtipunan_wl_img_status.setVisibility(1)

if wl_nagtipunan_stat == "NORMAL":
    nagtipunan_wl_img_status.setSymbol(NORMAL)
elif wl_nagtipunan_stat == "ALERT":
    nagtipunan_wl_img_status.setSymbol(ALERT)
elif wl_nagtipunan_stat == "ALARM":
    nagtipunan_wl_img_status.setSymbol(ALARM)
elif wl_nagtipunan_stat == "CRITICAL":
    nagtipunan_wl_img_status.setSymbol(CRITICAL)
else:
    nagtipunan_wl_img_status.setSymbol(NORMAL)

piat_wl_img_status = layout.itemById(PIAT_WL_STAT)
piat_wl_img_status.setVisibility(1)

if wl_piat_stat == "NORMAL":
    piat_wl_img_status.setSymbol(NORMAL)
elif wl_piat_stat == "ALERT":
    piat_wl_img_status.setSymbol(ALERT)
elif wl_piat_stat == "ALARM":
    piat_wl_img_status.setSymbol(ALARM)
elif wl_piat_stat == "CRITICAL":
    piat_wl_img_status.setSymbol(CRITICAL)
else:
    piat_wl_img_status.setSymbol(NORMAL)
"""

#base_path = os.path.join()
svg_path = os.path.join(str(current_dir) + "\\out\\svg", str(today) + "-cag_data.svg")
png_path = os.path.join(str(current_dir) + "\\out\\png", str(today) + "-cag_data.png")
pdf_path = os.path.join(str(current_dir) + "\\out\\pdf", str(today) + "-cag_data.pdf")

exporter = QgsLayoutExporter(layout)
exporter.exportToSvg(svg_path, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

print("done")

##########################  HF TEMPLATE
"""
print("Enter string for bulletin")
lines2 = sys.stdin.readlines()
status2 = "".join(lines) # Join the list of lines back into a single string
"""

for line in content2:
    if "FB No:" in line:
        fb_number_line = line.strip("\n").split(": ")[1]
        print(fb_number_line)
    elif "Issuance" in line:
        issuance = line.strip("\n").split(": ")[1]
        print(issuance)
    elif "Valid Until" in line:
        validity = line.strip("\n").split(": ")[1]
        print(validity)
    elif "Weather System" in line:
        w_system = line.strip("\n").split(": ")[1]
        print(w_system)
    elif "Ave_RF" in line:
        ave_rf = line.strip("\n").split(": ")[1]
        print(ave_rf)
    elif "Fcst_RF" in line:
        fcst_rf = line.strip("\n").split(": ")[1]
        print(fcst_rf)
    #wl value
    elif "BUNTUN WL" in line:
        buntun_val = line.strip("\n").split(": ")[1]
        print(buntun_val)
    elif "PIAT WL" in line:
        piat_val = line.strip("\n").split(": ")[1]
        print(piat_val)
    elif "GAMU WL" in line:
        gamu_val = line.strip("\n").split(": ")[1]
        print(gamu_val)
    elif "TUMAUINI WL" in line:
        tumauini_val = line.strip("\n").split(": ")[1]
        print(tumauini_val)
    elif "MARIS WL" in line:
        maris_val = line.strip("\n").split(": ")[1]
        print(maris_val)
    elif "PANGAL WL" in line:
        pangal_val = line.strip("\n").split(": ")[1]
        print(pangal_val)
    #impacts
    elif "buntun_impacts" in line:
        buntun_imp = line.strip("\n").split(": ")[1]
        print(buntun_imp)
    elif "piat_impacts" in line:
        piat_imp = line.strip("\n").split(": ")[1]
        print(piat_imp)
    elif "gamu_impacts" in line:
        gamu_imp = line.strip("\n").split(": ")[1]
        print(gamu_imp)
    elif "tumauini_impacts" in line:
        tumauini_imp = line.strip("\n").split(": ")[1]
        print(tumauini_imp)
    elif "maris_impacts" in line:
        maris_imp = line.strip("\n").split(": ")[1]
        print(maris_imp)
    elif "pangal_impacts" in line:
        pangal_imp = line.strip("\n").split(": ")[1]
        print(pangal_imp)
    elif "magat_gate" in line:
        magat_gate = line.strip("\n").split(": ")[1]
        print(magat_gate)
        

layoutHF = QgsPrintLayout(project)
layoutHF.initializeDefaults()

documentHF = QDomDocument()

## read template content
template_fileHF = open(str(current_dir) + "\\bulletin_template.qpt")
template_content = template_fileHF.read()
template_fileHF.close()
documentHF.setContent(template_content)


## load layout from template and add to Layout Manager
layoutHF.loadFromTemplate(documentHF, QgsReadWriteContext()) 
project.layoutManager().addLayout(layoutHF)


layoutHF = QgsProject.instance().layoutManager().layoutByName("bulletin1")

#layoutITEMS
station_status_img = layoutHF.itemById("crb_map")
fb_number = layoutHF.itemById("fb_no")
weather_system = layoutHF.itemById("weather_system")
ave_rainfall = layoutHF.itemById("ave_rainfall")
fcst_rainfall = layoutHF.itemById("fcst_rainfall")
dam_gate_opening = layoutHF.itemById("dam_gate_opening")
issuance_date = layoutHF.itemById("issuance_date")
valid_until = layoutHF.itemById("valid_until")

stat_buntun_color = layoutHF.itemById("stat_buntun_color")
stat_piat_color = layoutHF.itemById("stat_piat_color")
stat_gamu_color = layoutHF.itemById("stat_gamu_color")
stat_tumauini_color = layoutHF.itemById("stat_tumauini_color")
stat_maris_color = layoutHF.itemById("stat_maris_color")
stat_pangal_color = layoutHF.itemById("stat_pangal_color")

buntun_wl_val = layoutHF.itemById("buntun_wl_val")
piat_wl_val = layoutHF.itemById("piat_wl_val")
gamu_wl_val = layoutHF.itemById("gamu_wl_val")
tumauini_wl_val = layoutHF.itemById("tumauini_wl_val")
maris_wl_val = layoutHF.itemById("maris_wl_val")
pangal_wl_val = layoutHF.itemById("pangal_wl_val")

buntun_wl_stat2 = layoutHF.itemById("buntun_wl_stat2")
piat_wl_stat2 = layoutHF.itemById("piat_wl_stat2")
gamu_wl_stat2 = layoutHF.itemById("gamu_wl_stat2")
tumauini_wl_stat2 = layoutHF.itemById("tumauini_wl_stat2")
maris_wl_stat2 = layoutHF.itemById("maris_wl_stat2")
pangal_wl_stat2 = layoutHF.itemById("pangal_wl_stat2")

impact_buntun = layoutHF.itemById("impact_buntun")
impact_piat = layoutHF.itemById("impact_piat")
impact_gamu = layoutHF.itemById("impact_gamu")
impact_tumauini = layoutHF.itemById("impact_tumauini")
impact_maris = layoutHF.itemById("impact_maris")
impact_pangal = layoutHF.itemById("impact_pangal")


#update texts
fb_number.setText(fb_number_line)
weather_system.setText(w_system)
ave_rainfall.setText(ave_rf)
fcst_rainfall.setText(fcst_rf)
dam_gate_opening.setText(magat_gate)
issuance_date.setText(issuance)
valid_until.setText(validity)

buntun_wl_val.setText(buntun_val)
piat_wl_val.setText(piat_val)
gamu_wl_val.setText(gamu_val)
tumauini_wl_val.setText(tumauini_val)
maris_wl_val.setText(maris_val)
pangal_wl_val.setText(pangal_val)

impact_buntun.setText(buntun_imp)
impact_piat.setText(piat_imp)
impact_gamu.setText(gamu_imp)
impact_tumauini.setText(tumauini_imp)
impact_maris.setText(maris_imp)
impact_pangal.setText(pangal_imp)


buntun_wl_stat2.setText(wl_buntun_stat)
piat_wl_stat2.setText(wl_piat_stat)
gamu_wl_stat2.setText(wl_gamu_stat)
tumauini_wl_stat2.setText(wl_tumauini_stat)
maris_wl_stat2.setText("CRITICAL")
pangal_wl_stat2.setText(wl_pangal_stat)

"""
if wl_buntun_stat == "NORMAL":
    stat_buntun_color.setSymbol(NORMAL)
elif wl_buntun_stat == "ALERT":
    stat_buntun_color.setSymbol(ALERT)
elif wl_buntun_stat == "ALARM":
    stat_buntun_color.setSymbol(ALARM)
elif wl_buntun_stat == "CRITICAL":
    stat_buntun_color.setSymbol(CRITICAL)
else:
    stat_buntun_color.setSymbol(NORMAL)
"""

x_stat_color(wl_buntun_stat,stat_buntun_color)
x_stat_color(wl_piat_stat,stat_piat_color)
x_stat_color(wl_gamu_stat,stat_gamu_color)
x_stat_color(wl_tumauini_stat,stat_tumauini_color)
#x_stat_color(wl_maris_stat,stat_maris_color)
x_stat_color(wl_pangal_stat,stat_pangal_color)



folder_path = str(current_dir) + "\\out\\svg\\"
filename = str(today) + "-cag_data.svg"


station_status_img.setPicturePath(folder_path + filename)
#station_status_img.refreshPicture()

svg_path2 = os.path.join(str(current_dir) + "\\out2\\svg", str(today) + "-crb_data.svg")
png_path2 = os.path.join(str(current_dir) + "\\out2\\png", str(today) + "-crb_data.png")
pdf_path2 = os.path.join(str(current_dir) + "\\out2\\pdf", str(today) + "-crb_data.pdf")

exporter = QgsLayoutExporter(layoutHF)
exporter.exportToSvg(svg_path2, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path2, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path2, QgsLayoutExporter.PdfExportSettings())
print("done")

qgs.exitQgis()

#########################################################
