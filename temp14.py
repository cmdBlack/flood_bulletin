"""
Description: A script to automate generation of Daily Hydrological Forecast
             for Abra River Basin located in Northern Luzon Philippines.
            
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
#wl_naquino = "NSC"

with open("input1.txt", "r") as file1:
    content1 = file1.readlines()
    
with open("input2.txt", "r") as file2:
    content2 = file2.readlines()

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

"""
if "possible" in content1_single_string:
    yellow_mun = content1_single_string.split("possible[")[1].split("]")[0]
    yellow_mun = "".join(yellow_mun.split()).split(',')
    yellow_mun = [mun.lower() for mun in yellow_mun]
    print(yellow_mun)
elif "threatening" in content1_single_string:
    orange_mun = content1_single_string.split("threatening[")[1].split("]")[0]
    orange_mun = "".join(orange_mun.split()).split(',')
    orange_mun = [mun.lower() for mun in orange_mun]
    print(orange_mun)
elif "occur" in content1_single_string:
    red_mun = content1_single_string.split("occur[")[1].split("]")[0]
    red_mun = "".join(red_mun.split()).split(',')
    red_mun = [mun.lower() for mun in red_mun]
    print(red_mun)
elif "persisting" in content1_single_string:
    purple_mun = content1_single_string.split("persisting[")[1].split("]")[0]
    purple_mun = "".join(purple_mun.split()).split(',')
    purple_mun = [mun.lower() for mun in purple_mun]
    print(purple_mun)
elif "affecting" in content1_single_string:
    affecting_mun = content1_single_string.split("affecting[")[1].split("]")[0]
    affecting_mun = "".join(affecting_mun.split()).split(',')
    affecting_mun = [mun.lower() for mun in affecting_mun]
    print(affecting_mun)
else:
    pass

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
    elif "NAQUINO" in line:
        naquino_line = line.strip("\n").split("-")
        wl_naquino_stat = naquino_line[1]
        wl_naquino = naquino_line[2] 
    #elif "possible" in line:
    #    yellow_mun = line.split("possible[")[1].split("]")[0].split(",")
    #    yellow_mun = [mun.lower() for mun in yellow_mun]
    #    print(yellow_mun)
    #elif "threatening" in line:
    #    orange_mun = line.split("threatening[")[1].split("]")[0].split(",")
    #    orange_mun = [mun.lower() for mun in orange_mun]
    #    print(orange_mun)
    #elif "occur" in line:
    #    red_mun = line.split("occur[")[1].split("]")[0].split(",")
    #    red_mun = [mun.lower() for mun in red_mun]
    #    print(red_mun)
    #elif "persisting" in line:
    #    purple_mun = line.split("persisting[")[1].split("]")[0].split(",")
    #    purple_mun = [mun.lower() for mun in purple_mun]
    #    print(purple_mun)
    #elif "affecting" in line:
    #    affecting_mun = line.split("affecting[")[1].split("]")[0].split(",")
    #    affecting_mun = [mun.lower() for mun in affecting_mun]
    #    print(affecting_mun)
    else:
        pass

print("\n")
"""
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
"""
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
template_file = open(str(current_dir) + "\\crb_template3.qpt")

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
#wl_naquino = "NSC"

BUNTUN_WL_STAT = wl_buntun + "_BUNTUN"
TUMAUINI_WL_STAT = wl_tumauini + "_TUMAUINI"
GAMU_WL_STAT = wl_gamu + "_GAMU"

PARED_WL_STAT = wl_pared + "_PARED"
PENABLANCA_WL_STAT = wl_penablanca + "_PENABLANCA"
TABUK_WL_STAT = wl_tabuk + "_TABUK"
ANGADANAN_WL_STAT = wl_angadanan + "_ANGADANAN"
PANGAL_WL_STAT = wl_pangal + "_PANGAL"
NAGTIPUNAN_WL_STAT = wl_nagtipunan + "_NAGTIPUNAN"
NAQUINO_WL_STAT = wl_naquino + "_NAQUINO"

layout = QgsProject.instance().layoutManager().layoutByName("cagayan3")

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
naquino_wl_img_status = layout.itemById(NAQUINO_WL_STAT)
naquino_wl_img_status.setVisibility(1)



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
x_stat_color(wl_naquino_stat,naquino_wl_img_status)


#base_path = os.path.join()
svg_path = os.path.join(str(current_dir) + "\\out\\svg", str(today) + "-cag_data.svg")
png_path = os.path.join(str(current_dir) + "\\out\\png", str(today) + "-cag_data.png")
pdf_path = os.path.join(str(current_dir) + "\\out\\pdf", str(today) + "-cag_data.pdf")

exporter = QgsLayoutExporter(layout)
exporter.exportToSvg(svg_path, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

print("DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP")

##########################  HF TEMPLATE
"""
print("Enter string for bulletin")
lines2 = sys.stdin.readlines()
status2 = "".join(lines) # Join the list of lines back into a single string
"""

for line in content2:
    if "FB No:" in line:
        fb_number_line = line.strip("\n").split(": ")[1]
    elif "Issuance" in line:
        issuance = line.strip("\n").split(": ")[1]
    elif "Valid Until" in line:
        validity = line.strip("\n").split(": ")[1]
    elif "Weather System" in line:
        w_system = line.strip("\n").split(": ")[1]
    elif "Ave_RF" in line:
        ave_rf = line.strip("\n").split(": ")[1]
    elif "Fcst_RF" in line:
        fcst_rf = line.strip("\n").split(": ")[1]
    #wl value
    elif "BUNTUN WL" in line:
        buntun_val = line.strip("\n").split(": ")[1]
    elif "NAQUINO WL" in line:
        naquino_val = line.strip("\n").split(": ")[1]
    elif "GAMU WL" in line:
        gamu_val = line.strip("\n").split(": ")[1]
    elif "TUMAUINI WL" in line:
        tumauini_val = line.strip("\n").split(": ")[1]
    elif "PANGAL WL" in line:
        pangal_val = line.strip("\n").split(": ")[1]
    #impacts
    elif "buntun_impacts" in line:
        buntun_imp = line.strip("\n").split(": ")[1]
    elif "naquino_impacts" in line:
        naquino_imp = line.strip("\n").split(": ")[1]
    elif "gamu_impacts" in line:
        gamu_imp = line.strip("\n").split(": ")[1]
    elif "tumauini_impacts" in line:
        tumauini_imp = line.strip("\n").split(": ")[1]
    elif "pangal_impacts" in line:
        pangal_imp = line.strip("\n").split(": ")[1]
    #addtl messsage
    elif "buntun_addtl" in line:
        addtl_buntun_text = line.strip("\n").split(": ")[1]
    elif "naquino_addtl" in line:
        addtl_naquino_text = line.strip("\n").split(": ")[1]
    elif "gamu_addtl" in line:
        addtl_gamu_text = line.strip("\n").split(": ")[1]
    elif "tumauini_addtl" in line:
        addtl_tumauini_text = line.strip("\n").split(": ")[1]
    elif "pangal_addtl" in line:
        addtl_pangal_text = line.strip("\n").split(": ")[1]

    # extras
    elif "magat_gate" in line:
        magat_gate = line.strip("\n").split(": ")[1]
    elif "signature" in line:
        sign = line.strip("\n").split(": ")[1]
        signs_lst = "".join(sign.split()).split("/")
        print(signs_lst)
    elif "FLOOD THREAT MSG" in line:
        fthreat_txt = line.strip("\n").split(": ")[1]
    elif "FTHREAT MSG TAGALOG" in line:
        fthreat_tg_txt = line.strip("\n").split(": ")[1]
    """
    elif "fsize" in line:
        font_size = int(line.strip("\n").split(": ")[1])
        print(font_size)
    """ 

layoutHF = QgsPrintLayout(project)
layoutHF.initializeDefaults()

documentHF = QDomDocument()

## read template content
template_fileHF = open(str(current_dir) + "\\bulletin_template3.qpt")
template_content = template_fileHF.read()
template_fileHF.close()
documentHF.setContent(template_content)


## load layout from template and add to Layout Manager
layoutHF.loadFromTemplate(documentHF, QgsReadWriteContext()) 
project.layoutManager().addLayout(layoutHF)


layoutHF = QgsProject.instance().layoutManager().layoutByName("bulletin3")

#layoutITEMS
station_status_img = layoutHF.itemById("crb_map")
fb_number = layoutHF.itemById("fb_no")
weather_system = layoutHF.itemById("weather_system")
ave_rainfall = layoutHF.itemById("ave_rainfall")
fcst_rainfall = layoutHF.itemById("fcst_rainfall")
dam_gate_opening = layoutHF.itemById("dam_gate_opening")
issuance_date = layoutHF.itemById("issuance_date")
valid_until = layoutHF.itemById("valid_until")

fthreat = layoutHF.itemById("fthreat")
fthreat_tg = layoutHF.itemById("fthreat_tg")

stat_buntun_color = layoutHF.itemById("stat_buntun_color")
stat_naquino_color = layoutHF.itemById("stat_naquino_color")
stat_gamu_color = layoutHF.itemById("stat_gamu_color")
stat_tumauini_color = layoutHF.itemById("stat_tumauini_color")
stat_pangal_color = layoutHF.itemById("stat_pangal_color")

buntun_wl_val = layoutHF.itemById("buntun_wl_val")
naquino_wl_val = layoutHF.itemById("naquino_wl_val")
gamu_wl_val = layoutHF.itemById("gamu_wl_val")
tumauini_wl_val = layoutHF.itemById("tumauini_wl_val")
pangal_wl_val = layoutHF.itemById("pangal_wl_val")

buntun_wl_stat2 = layoutHF.itemById("buntun_wl_stat2")
naquino_wl_stat2 = layoutHF.itemById("naquino_wl_stat2")
gamu_wl_stat2 = layoutHF.itemById("gamu_wl_stat2")
tumauini_wl_stat2 = layoutHF.itemById("tumauini_wl_stat2")
pangal_wl_stat2 = layoutHF.itemById("pangal_wl_stat2")

impact_buntun = layoutHF.itemById("impact_buntun")
impact_naquino = layoutHF.itemById("impact_naquino")
impact_gamu = layoutHF.itemById("impact_gamu")
impact_tumauini = layoutHF.itemById("impact_tumauini")
impact_pangal = layoutHF.itemById("impact_pangal")

addtl_buntun = layoutHF.itemById("addtl_buntun")
addtl_naquino = layoutHF.itemById("addtl_naquino")
addtl_gamu = layoutHF.itemById("addtl_gamu")
addtl_tumauini = layoutHF.itemById("addtl_tumauini")
addtl_pangal = layoutHF.itemById("addtl_pangal")

signature = layoutHF.itemById("signature")

"""
sig1 = layoutHF.itemById("sig1")
sig2 = layoutHF.itemById("sig2")
sig3 = layoutHF.itemById("sig3")
sig4 = layoutHF.itemById("sig4")
sig5 = layoutHF.itemById("sig5")
sig6 = layoutHF.itemById("sig6")
"""

#update texts
fb_number.setText(fb_number_line)
weather_system.setText(w_system)
ave_rainfall.setText(ave_rf)
fcst_rainfall.setText(fcst_rf)
dam_gate_opening.setText(magat_gate)
issuance_date.setText(issuance)
valid_until.setText(validity)

buntun_wl_val.setText(buntun_val)
naquino_wl_val.setText(naquino_val)
gamu_wl_val.setText(gamu_val)
tumauini_wl_val.setText(tumauini_val)
pangal_wl_val.setText(pangal_val)

impact_buntun.setText(buntun_imp)
text_format.setSize(adjust_fsize(buntun_imp))
impact_buntun.setTextFormat(text_format)

impact_naquino.setText(naquino_imp)
text_format.setSize(adjust_fsize(naquino_imp))
impact_naquino.setTextFormat(text_format)

impact_gamu.setText(gamu_imp)
text_format.setSize(adjust_fsize(gamu_imp))
impact_gamu.setTextFormat(text_format)

impact_tumauini.setText(tumauini_imp)
text_format.setSize(adjust_fsize(tumauini_imp))
impact_tumauini.setTextFormat(text_format)

impact_pangal.setText(pangal_imp)
text_format.setSize(adjust_fsize(pangal_imp))
impact_pangal.setTextFormat(text_format)
"""
buntun_wl_stat2.setText(wl_buntun_stat)
naquino_wl_stat2.setText(wl_naquino_stat)
gamu_wl_stat2.setText(wl_gamu_stat)
tumauini_wl_stat2.setText(wl_tumauini_stat)
pangal_wl_stat2.setText(wl_pangal_stat)
"""

x_normal_balert(wl_buntun_stat,buntun_wl_stat2)
x_normal_balert(wl_naquino_stat,naquino_wl_stat2)
x_normal_balert(wl_gamu_stat,gamu_wl_stat2)
x_normal_balert(wl_tumauini_stat,tumauini_wl_stat2)
x_normal_balert(wl_pangal_stat,pangal_wl_stat2)



addtl_buntun.setText(addtl_buntun_text)
addtl_naquino.setText(addtl_naquino_text)
addtl_gamu.setText(addtl_gamu_text)
addtl_tumauini.setText(addtl_tumauini_text)
addtl_pangal.setText(addtl_pangal_text)

signature.setText(sign)
"""
def attach_signature(sig_img,lst):
    for sig_txt in lst:
        sig_img.setPicturePath(str(current_dir) + "\\signatures\\" + sig_txt + "_sig.png")
"""

for index, sig in enumerate(signs_lst,start=1):
    sig_img = layoutHF.itemById("sig" + str(index))
    sig_path = str(current_dir) + "\\signatures\\" + signs_lst[index-1] + "_sig.png"
    #sig_img.setPicturePath(sig_path)
    #sig_img.setPicturePath(str(current_dir) + "\\signatures\\" + signs_lst[index-1] + "_sig.png")
    # Set path only if file exists
    if os.path.isfile(sig_path):
      sig_img.setPicturePath(sig_path)
    else:
      print("NO SIGNATURE PNG FILE EXISTS FOR " + sig)
      pass


fthreat.setText(fthreat_txt)
fthreat_tg.setText(fthreat_tg_txt)


x_stat_color(wl_buntun_stat,stat_buntun_color)
x_stat_color(wl_naquino_stat,stat_naquino_color)
x_stat_color(wl_gamu_stat,stat_gamu_color)
x_stat_color(wl_tumauini_stat,stat_tumauini_color)
x_stat_color(wl_pangal_stat,stat_pangal_color)

"""
#text_format_whitefont
if stat == "NORMAL" or stat == "CRITICAL":
    stat.setTextFormat(text_format_whitefont)
else:
    pass
"""
x_fcolor(wl_buntun_stat,buntun_wl_stat2)
x_fcolor(wl_naquino_stat,naquino_wl_stat2)
x_fcolor(wl_gamu_stat,gamu_wl_stat2)
x_fcolor(wl_tumauini_stat,tumauini_wl_stat2)
x_fcolor(wl_pangal_stat,pangal_wl_stat2)



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


print("DONE BULLETIN  DONE BULLETIN  DONE BULLETIN  DONE BULLETIN  DONE BULLETIN")

qgs.exitQgis()

#########################################################
