"""
Description: A script to automate generation of Flood Bulletin
             for Apayao Abulug River Basin located in Northern Luzon Philippines.
            
AUTHOR: KAIZER MACNI

"""

import os
import warnings
import sys
import re
#from tqdm import tqdm

# SUPPRESS WARNINGS ON TERMINAL
from osgeo import gdal
gdal.PushErrorHandler('CPLQuietErrorHandler')

from qgis.PyQt.QtCore import qInstallMessageHandler
def silent_handler(msg_type, msg_log_context, msg_string):
    pass
qInstallMessageHandler(silent_handler)


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
from PyQt5.QtGui import QFont


from datetime import date
from datetime import datetime

os.environ["PROJ_LIB"] = "C:\\OSGeo4W\\share\\proj"

#COURTESY
print("BY: NLPRSD HTC 2026")
print("programmed by: KMacni\n")

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

def adjust_fsize(txt):
    char_cnt = len(txt)

    if char_cnt < 20:
        return 45
    elif char_cnt < 30:
        return 40
    elif char_cnt < 51:
        return 37
    else:
        return 32

def x_fcolor(stat,stat_item):
    #text_format_whitefont
    if stat == "NORMAL" or stat == "CRITICAL":
        stat_item.setTextFormat(text_format_whitefont)
    else:
        pass

def x_normal_balert(stat,stat_item):
    if stat == "NORMAL":
        stat_item.setText("Status: BELOW ALERT")
    else:
        stat_item.setText("Status: " + stat)

def attach_signature(sig_img,lst):
    for sig_txt in lst:
        print(sig_img)
        sig_img.setPicturePath(str(current_dir) + "\\signatures\\" + sig_txt + "_sig.png")

with open("input1.txt", "r") as file1:
    content1 = file1.readlines()

content1_single_string = "".join(content1)

if "possible" in content1_single_string:
    yellow_mun = content1_single_string.split("possible[")[1].split("]")[0]
    yellow_mun = "".join(yellow_mun.split()).split(',')
    yellow_mun = [mun.lower() for mun in yellow_mun]
    print(yellow_mun)
if "threatening" in content1_single_string:
    orange_mun = content1_single_string.split("threatening[")[1].split("]")[0]
    orange_mun = "".join(orange_mun.split()).split(',')
    orange_mun = [mun.lower() for mun in orange_mun]
    print(orange_mun)
if "occur" in content1_single_string:
    red_mun = content1_single_string.split("occur[")[1].split("]")[0]
    red_mun = "".join(red_mun.split()).split(',')
    red_mun = [mun.lower() for mun in red_mun]
    print(red_mun)
if "persisting" in content1_single_string:
    purple_mun = content1_single_string.split("persisting[")[1].split("]")[0]
    purple_mun = "".join(purple_mun.split()).split(',')
    purple_mun = [mun.lower() for mun in purple_mun]
    print(purple_mun)
if "affecting" in content1_single_string:
    affecting_mun = content1_single_string.split("affecting[")[1].split("]")[0]
    affecting_mun = "".join(affecting_mun.split()).split(',')
    affecting_mun = [mun.lower() for mun in affecting_mun]
    print(affecting_mun)


for line in content1:
    if "PUDTOL" in line:
        pudtol_line = line.strip("\n").split("-")
        wl_pudtol_stat = pudtol_line[1]
        wl_pudtol = pudtol_line[2]
    elif "MATON" in line:
        maton_line = line.strip("\n").split("-")
        wl_maton_stat = maton_line[1]
        wl_maton = maton_line[2]
    elif "BUBULAYAN" in line:
        bubulayan_line = line.strip("\n").split("-")
        wl_bubulayan_stat = bubulayan_line[1]
        wl_bubulayan = bubulayan_line[2]
    elif "PACO" in line:
        paco_line = line.strip("\n").split("-")
        wl_paco_stat = paco_line[1]
        wl_paco = paco_line[2]
    elif "LUCBAN" in line:
        lucban_line = line.strip("\n").split("-")
        wl_lucban_stat = lucban_line[1]
        wl_lucban = lucban_line[2]
    elif "GUIDDAM" in line:
        guiddam_line = line.strip("\n").split("-")
        wl_guiddam_stat = guiddam_line[1]
        wl_guiddam = guiddam_line[2]
    elif "MALUBIBIT" in line:
        malubibit_line = line.strip("\n").split("-")
        wl_malubibit_stat = malubibit_line[1]
        wl_malubibit = malubibit_line[2]
    else:
        pass

print("\n")

###########################################################


app = QApplication([])
#qgs.setPrefixPath("C:\\OSGeo4W\\apps\\qgis-ltr", True)
QgsApplication.setPrefixPath("C:\\OSGeo4W\\apps\\qgis-ltr", True)
qgs = QgsApplication([], False)


qgs.initQgis()

canvas = QgsMapCanvas()

project = QgsProject.instance()
bridge = QgsLayerTreeMapCanvasBridge(project.layerTreeRoot(), canvas)

current_dir = Path.cwd()

# Create the directory and any missing parent directories
os.makedirs(str(current_dir) + "\\out\\png", exist_ok=True)
os.makedirs(str(current_dir) + "\\out\\svg", exist_ok=True)
os.makedirs(str(current_dir) + "\\out\\pdf", exist_ok=True)

os.makedirs(str(current_dir) + "\\out2\\png", exist_ok=True)
os.makedirs(str(current_dir) + "\\out2\\svg", exist_ok=True)
os.makedirs(str(current_dir) + "\\out2\\pdf", exist_ok=True)


project.read(str(current_dir) + "\\apayao_abulug.qgz")

layer = project.mapLayersByName('apayaoAbulugMunicities')[0]

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
        elif mun_name in affecting_mun:
            feature['flood_cat'] = 11
        else:
            feature['flood_cat'] = 0


        layer.updateFeature(feature)
        up_flood = feature.attribute('flood_cat')



today = date.today()
crt = datetime.now().strftime("%H:%M")
#today = "2024-10-03"

# Create a QgsTextFormat object
text_format = QgsTextFormat()

text_format_whitefont = QgsTextFormat()
text_format_whitefont.setColor(QColor('white'))
text_format_whitefont.setSize(36)
text_format_whitefont.setForcedBold(True)


# Create a QFont object
font = QFont()
font.setFamily("Arial")  # Or any other font family you prefer

text_format.setFont(font)


project = QgsProject.instance()
            
manager = project.layoutManager()
layouts_list = manager.printLayouts()




layout = QgsPrintLayout(project)
layout.initializeDefaults()

        
document = QDomDocument()

# read template content
template_file = open(str(current_dir) + "\\apb_template.qpt")

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


PUDTOL_WL_STAT = wl_pudtol + "_PUDTOL"
MATON_WL_STAT = wl_maton + "_MATON"
BUBULAYAN_WL_STAT = wl_bubulayan + "_BUBULAYAN"
PACO_WL_STAT = wl_paco + "_PACO"
LUCBAN_WL_STAT = wl_lucban + "_LUCBAN"
GUIDDAM_WL_STAT = wl_guiddam + "_GUIDDAM"
MALUBIBIT_WL_STAT = wl_malubibit + "_MALUBIBIT"

layout = QgsProject.instance().layoutManager().layoutByName("apayaoabulug")

#waterlevels
pudtol_wl_img_status = layout.itemById(PUDTOL_WL_STAT)
pudtol_wl_img_status.setVisibility(1)
maton_wl_img_status = layout.itemById(MATON_WL_STAT)
maton_wl_img_status.setVisibility(1)
bubulayan_wl_img_status = layout.itemById(BUBULAYAN_WL_STAT)
bubulayan_wl_img_status.setVisibility(1)
paco_wl_img_status = layout.itemById(PACO_WL_STAT)
paco_wl_img_status.setVisibility(1)
lucban_wl_img_status = layout.itemById(LUCBAN_WL_STAT)
lucban_wl_img_status.setVisibility(1)
guiddam_wl_img_status = layout.itemById(GUIDDAM_WL_STAT)
guiddam_wl_img_status.setVisibility(1)
malubibit_wl_img_status = layout.itemById(MALUBIBIT_WL_STAT)
malubibit_wl_img_status.setVisibility(1)

x_stat_color(wl_pudtol_stat,pudtol_wl_img_status)
x_stat_color(wl_maton_stat,maton_wl_img_status)
x_stat_color(wl_bubulayan_stat,bubulayan_wl_img_status)
x_stat_color(wl_paco_stat,paco_wl_img_status)
x_stat_color(wl_lucban_stat,lucban_wl_img_status)
x_stat_color(wl_guiddam_stat,guiddam_wl_img_status)
x_stat_color(wl_malubibit_stat,malubibit_wl_img_status)



#base_path = os.path.join()
svg_path = os.path.join(str(current_dir) + "\\out\\svg", str(today) + "-apb_data.svg")
png_path = os.path.join(str(current_dir) + "\\out\\png", str(today) + "-apb_data.png")
pdf_path = os.path.join(str(current_dir) + "\\out\\pdf", str(today) + "-apb_data.pdf")

exporter = QgsLayoutExporter(layout)
exporter.exportToSvg(svg_path, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

print("DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP")

##########################  HF TEMPLATE


qgs.exitQgis()

#########################################################
