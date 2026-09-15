"""
Description: A script to automate generation of Flood Bulletin
             for Laoag River Basin located in Northern Luzon Philippines.
            
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
from qgis.PyQt.QtCore import Qt


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

def x_stat_bgcolor(stat,color):
    if stat == "NORMAL":
        #color.setSymbol(NORMAL)
        color.setBackgroundColor(QColor("green"))
    elif stat == "ALERT":
        #color.setSymbol(ALERT)
        color.setBackgroundColor(QColor("yellow"))
    elif stat == "ALARM":
        #color.setSymbol(ALARM)
        color.setBackgroundColor(QColor("orange"))
    elif stat == "CRITICAL":
        #color.setSymbol(CRITICAL)
        color.setBackgroundColor(QColor("red"))
    else:
        #color.setSymbol(NORMAL)
        color.setBackgroundColor(QColor("green"))

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

def x_fcolor2(stat,stat_item):
    #text_format_whitefont
    if stat == "NORMAL" or stat == "CRITICAL":
        stat_item.setTextFormat(text_format_whitefont2)
    else:
        pass


def x_normal_balert(stat,stat_item):
    if stat == "NORMAL":
        stat_item.setText("BELOW ALERT")
    else:
        stat_item.setText(stat)

def x_normal_balert2(stat,stat_item):
    if stat == "NORMAL":
        stat_item.setText("Status: BELOW ALERT")
    else:
        stat_item.setText("Status: " + stat)

def attach_signature(sig_img,lst):
    for sig_txt in lst:
        print(sig_img)
        sig_img.setPicturePath(str(current_dir) + "\\signatures\\" + sig_txt + "_sig.png")

def appear(name):
    pline = layout.itemById(name + "_PLINE")
    pline.setVisibility(1)
    label = layout.itemById(name + "_LABEL")
    label.setVisibility(1)
    rect = layout.itemById(name + "_RECT")
    rect.setVisibility(1)
    status = layout.itemById(name + "_STATUS")
    status.setVisibility(1)
        

with open("input1_bulletin_adv.txt", "r") as file1:
    content1 = file1.readlines()
    
with open("input2_bulletin_adv.txt", "r") as file2:
    content2 = file2.readlines()


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
for line in content1:
    if "GILBERT" in line:
        gilbert_line = line.strip("\n").split("-")
        wl_gilbert_stat = gilbert_line[1]
        wl_gilbert = gilbert_line[2]
        appear("GILBERT")
    elif "ARANIW" in line:
        araniw_line = line.strip("\n").split("-")
        wl_araniw_stat = araniw_line[1]
        wl_araniw = araniw_line[2]
        appear("ARANIW")
    elif "MANGATO" in line:
        mangato_line = line.strip("\n").split("-")
        wl_mangato_stat = mangato_line[1]
        wl_mangato = mangato_line[2]
        appear("MANGATO")
    elif "SARRAT" in line:
        sarrat_line = line.strip("\n").split("-")
        wl_sarrat_stat = sarrat_line[1]
        wl_sarrat = sarrat_line[2]
        appear("SARRAT")
    elif "DARASDAS" in line:
        darasdas_line = line.strip("\n").split("-")
        wl_darasdas_stat = darasdas_line[1]
        wl_darasdas = darasdas_line[2]
        appear("DARASDAS")
    elif "TABTABAGAN" in line:
        tabtabagan_line = line.strip("\n").split("-")
        wl_tabtabagan_stat = tabtabagan_line[1]
        wl_tabtabagan = tabtabagan_line[2]
        appear("TABTABAGAN")
    elif "BONGGO" in line:
        bonggo_line = line.strip("\n").split("-")
        wl_bonggo_stat = bonggo_line[1]
        wl_bonggo = bonggo_line[2]
        appear("BONGGO")
    elif "MADONGAN" in line:
        madongan_line = line.strip("\n").split("-")
        wl_madongan_stat = madongan_line[1]
        wl_madongan = madongan_line[2]
        appear("MADONGAN")
    elif "GASGAS" in line:
        gasgas_line = line.strip("\n").split("-")
        wl_gasgas_stat = gasgas_line[1]
        wl_gasgas = gasgas_line[2]
        appear("GASGAS")
    elif "MANALPAC" in line:
        manalpac_line = line.strip("\n").split("-")
        wl_manalpac_stat = manalpac_line[1]
        wl_manalpac = manalpac_line[2]
        appear("MANALPAC")
    elif "BAGBAG" in line:
        bagbag_line = line.strip("\n").split("-")
        wl_bagbag_stat = bagbag_line[1]
        wl_bagbag = bagbag_line[2]
        appear("BAGBAG")
    elif "CALLUSA" in line:
        callusa_line = line.strip("\n").split("-")
        wl_callusa_stat = callusa_line[1]
        wl_callusa = callusa_line[2]
        appear("CALLUSA")
    else:
        pass
"""
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


project.read(str(current_dir) + "\\laoag_riverbasin.qgz")

layer = project.mapLayersByName('laoagBASIN_mun')[0]

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
text_format_whitefont.setSize(12)
text_format_whitefont.setForcedBold(True)

text_format_whitefont2 = QgsTextFormat()
text_format_whitefont2.setColor(QColor('white'))
text_format_whitefont2.setSize(75)
text_format_whitefont2.setForcedBold(True)


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
template_file = open(str(current_dir) + "\\laoagrb_template.qpt")

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



layout = QgsProject.instance().layoutManager().layoutByName("laoag_map")


for line in content1:
    if "GILBERT" in line:
        gilbert_line = line.strip("\n").split("-")
        wl_gilbert_stat = gilbert_line[1]
        wl_gilbert = gilbert_line[2]
        appear("GILBERT")
        GILBERT_WL_STAT = wl_gilbert + "_GILBERT"
        gilbert_wl_img_status = layout.itemById(GILBERT_WL_STAT)
        gilbert_wl_img_status.setVisibility(1)
        x_stat_color(wl_gilbert_stat,gilbert_wl_img_status)

        gilbert_wl_stat2 = layout.itemById("GILBERT_STATUS")
        x_normal_balert(wl_gilbert_stat,gilbert_wl_stat2)
        x_fcolor(wl_gilbert_stat,gilbert_wl_stat2)
        x_stat_bgcolor(wl_gilbert_stat,gilbert_wl_stat2)
    elif "ARANIW" in line:
        araniw_line = line.strip("\n").split("-")
        wl_araniw_stat = araniw_line[1]
        wl_araniw = araniw_line[2]
        appear("ARANIW")
        ARANIW_WL_STAT = wl_araniw + "_ARANIW"
        araniw_wl_img_status = layout.itemById(ARANIW_WL_STAT)
        araniw_wl_img_status.setVisibility(1)
        x_stat_color(wl_araniw_stat,araniw_wl_img_status)

        araniw_wl_stat2 = layout.itemById("ARANIW_STATUS")
        x_normal_balert(wl_araniw_stat,araniw_wl_stat2)
        x_fcolor(wl_araniw_stat,araniw_wl_stat2)
        x_stat_bgcolor(wl_araniw_stat,araniw_wl_stat2)
    elif "MANGATO" in line:
        mangato_line = line.strip("\n").split("-")
        wl_mangato_stat = mangato_line[1]
        wl_mangato = mangato_line[2]
        appear("MANGATO")
        MANGATO_WL_STAT = wl_mangato + "_MANGATO"
        mangato_wl_img_status = layout.itemById(MANGATO_WL_STAT)
        mangato_wl_img_status.setVisibility(1)
        x_stat_color(wl_mangato_stat,mangato_wl_img_status)

        mangato_wl_stat2 = layout.itemById("MANGATO_STATUS")
        x_normal_balert(wl_mangato_stat,mangato_wl_stat2)
        x_fcolor(wl_mangato_stat,mangato_wl_stat2)
        x_stat_bgcolor(wl_mangato_stat,mangato_wl_stat2) 
    elif "SARRAT" in line:
        sarrat_line = line.strip("\n").split("-")
        wl_sarrat_stat = sarrat_line[1]
        wl_sarrat = sarrat_line[2]
        appear("SARRAT")
        SARRAT_WL_STAT = wl_sarrat + "_SARRAT"
        sarrat_wl_img_status = layout.itemById(SARRAT_WL_STAT)
        sarrat_wl_img_status.setVisibility(1)
        x_stat_color(wl_sarrat_stat,sarrat_wl_img_status)

        sarrat_wl_stat2 = layout.itemById("SARRAT_STATUS")
        x_normal_balert(wl_sarrat_stat,sarrat_wl_stat2)
        x_fcolor(wl_sarrat_stat,sarrat_wl_stat2)
        x_stat_bgcolor(wl_sarrat_stat,sarrat_wl_stat2) 
    elif "DARASDAS" in line:
        darasdas_line = line.strip("\n").split("-")
        wl_darasdas_stat = darasdas_line[1]
        wl_darasdas = darasdas_line[2]
        appear("DARASDAS")
        DARASDAS_WL_STAT = wl_darasdas + "_DARASDAS"
        darasdas_wl_img_status = layout.itemById(DARASDAS_WL_STAT)
        darasdas_wl_img_status.setVisibility(1)
        x_stat_color(wl_darasdas_stat,darasdas_wl_img_status)

        darasdas_wl_stat2 = layout.itemById("DARASDAS_STATUS")
        x_normal_balert(wl_darasdas_stat,darasdas_wl_stat2)
        x_fcolor(wl_darasdas_stat,darasdas_wl_stat2)
        x_stat_bgcolor(wl_darasdas_stat,darasdas_wl_stat2) 
    elif "TABTABAGAN" in line:
        tabtabagan_line = line.strip("\n").split("-")
        wl_tabtabagan_stat = tabtabagan_line[1]
        wl_tabtabagan = tabtabagan_line[2]
        appear("TABTABAGAN")
        TABTABAGAN_WL_STAT = wl_tabtabagan + "_TABTABAGAN"
        tabtabagan_wl_img_status = layout.itemById(TABTABAGAN_WL_STAT)
        tabtabagan_wl_img_status.setVisibility(1)
        x_stat_color(wl_tabtabagan_stat,tabtabagan_wl_img_status)

        tabtabagan_wl_stat2 = layout.itemById("TABTABAGAN_STATUS")
        x_normal_balert(wl_tabtabagan_stat,tabtabagan_wl_stat2)
        x_fcolor(wl_tabtabagan_stat,tabtabagan_wl_stat2)
        x_stat_bgcolor(wl_tabtabagan_stat,tabtabagan_wl_stat2) 
    elif "BONGGO" in line:
        bonggo_line = line.strip("\n").split("-")
        wl_bonggo_stat = bonggo_line[1]
        wl_bonggo = bonggo_line[2]
        appear("BONGGO")
        BONGGO_WL_STAT = wl_bonggo + "_BONGGO"
        bonggo_wl_img_status = layout.itemById(BONGGO_WL_STAT)
        bonggo_wl_img_status.setVisibility(1)
        x_stat_color(wl_bonggo_stat,bonggo_wl_img_status)

        bonggo_wl_stat2 = layout.itemById("BONGGO_STATUS")
        x_normal_balert(wl_bonggo_stat,bonggo_wl_stat2)
        x_fcolor(wl_bonggo_stat,bonggo_wl_stat2)
        x_stat_bgcolor(wl_bonggo_stat,bonggo_wl_stat2) 
    elif "MADONGAN" in line:
        madongan_line = line.strip("\n").split("-")
        wl_madongan_stat = madongan_line[1]
        wl_madongan = madongan_line[2]
        appear("MADONGAN")
        MADONGAN_WL_STAT = wl_madongan + "_MADONGAN"
        madongan_wl_img_status = layout.itemById(MADONGAN_WL_STAT)
        madongan_wl_img_status.setVisibility(1)
        x_stat_color(wl_madongan_stat,madongan_wl_img_status)

        madongan_wl_stat2 = layout.itemById("MADONGAN_STATUS")
        x_normal_balert(wl_madongan_stat,madongan_wl_stat2)
        x_fcolor(wl_madongan_stat,madongan_wl_stat2)
        x_stat_bgcolor(wl_madongan_stat,madongan_wl_stat2) 
    elif "GASGAS" in line:
        gasgas_line = line.strip("\n").split("-")
        wl_gasgas_stat = gasgas_line[1]
        wl_gasgas = gasgas_line[2]
        appear("GASGAS")
        GASGAS_WL_STAT = wl_gasgas + "_GASGAS"
        gasgas_wl_img_status = layout.itemById(GASGAS_WL_STAT)
        gasgas_wl_img_status.setVisibility(1)
        x_stat_color(wl_gasgas_stat,gasgas_wl_img_status)

        gasgas_wl_stat2 = layout.itemById("GASGAS_STATUS")
        x_normal_balert(wl_gasgas_stat,gasgas_wl_stat2)
        x_fcolor(wl_gasgas_stat,gasgas_wl_stat2)
        x_stat_bgcolor(wl_gasgas_stat,gasgas_wl_stat2) 
    elif "MANALPAC" in line:
        manalpac_line = line.strip("\n").split("-")
        wl_manalpac_stat = manalpac_line[1]
        wl_manalpac = manalpac_line[2]
        appear("MANALPAC")
        MANALPAC_WL_STAT = wl_manalpac + "_MANALPAC"
        manalpac_wl_img_status = layout.itemById(MANALPAC_WL_STAT)
        manalpac_wl_img_status.setVisibility(1)
        x_stat_color(wl_manalpac_stat,manalpac_wl_img_status)

        manalpac_wl_stat2 = layout.itemById("MANALPAC_STATUS")
        x_normal_balert(wl_manalpac_stat,manalpac_wl_stat2)
        x_fcolor(wl_manalpac_stat,manalpac_wl_stat2)
        x_stat_bgcolor(wl_manalpac_stat,manalpac_wl_stat2) 
    elif "BAGBAG" in line:
        bagbag_line = line.strip("\n").split("-")
        wl_bagbag_stat = bagbag_line[1]
        wl_bagbag = bagbag_line[2]
        appear("BAGBAG")
        BAGBAG_WL_STAT = wl_bagbag + "_BAGBAG"
        bagbag_wl_img_status = layout.itemById(BAGBAG_WL_STAT)
        bagbag_wl_img_status.setVisibility(1)
        x_stat_color(wl_bagbag_stat,bagbag_wl_img_status)

        bagbag_wl_stat2 = layout.itemById("BAGBAG_STATUS")
        x_normal_balert(wl_bagbag_stat,bagbag_wl_stat2)
        x_fcolor(wl_bagbag_stat,bagbag_wl_stat2)
        x_stat_bgcolor(wl_bagbag_stat,bagbag_wl_stat2) 
    elif "CALLUSA" in line:
        callusa_line = line.strip("\n").split("-")
        wl_callusa_stat = callusa_line[1]
        wl_callusa = callusa_line[2]
        appear("CALLUSA")
        CALLUSA_WL_STAT = wl_callusa + "_CALLUSA"
        callusa_wl_img_status = layout.itemById(CALLUSA_WL_STAT)
        callusa_wl_img_status.setVisibility(1)
        x_stat_color(wl_callusa_stat,callusa_wl_img_status)

        callusa_wl_stat2 = layout.itemById("CALLUSA_STATUS")
        x_normal_balert(wl_callusa_stat,callusa_wl_stat2)
        x_fcolor(wl_callusa_stat,callusa_wl_stat2)
        x_stat_bgcolor(wl_callusa_stat,callusa_wl_stat2) 
    else:
        pass

####  WATER LEVEL  #####################

#waterlevels


#base_path = os.path.join()
svg_path = os.path.join(str(current_dir) + "\\out\\svg", str(today) + "-laoag_data.svg")
png_path = os.path.join(str(current_dir) + "\\out\\png", str(today) + "-laoag_data.png")
pdf_path = os.path.join(str(current_dir) + "\\out\\pdf", str(today) + "-laoag_data.pdf")

exporter = QgsLayoutExporter(layout)
exporter.exportToSvg(svg_path, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

print("DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP DONE MAP")

##########################  HF TEMPLATE


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
    elif "GILBERT WL" in line:
        gilbert_val = line.strip("\n").split(": ")[1]
    elif "SARRAT WL" in line:
        sarrat_val = line.strip("\n").split(": ")[1]
    elif "DARASDAS WL" in line:
        darasdas_val = line.strip("\n").split(": ")[1]
    elif "TABTABAGAN WL" in line:
        tabtabagan_val = line.strip("\n").split(": ")[1]
    elif "CALLUSA WL" in line:
        callusa_val = line.strip("\n").split(": ")[1]
    elif "MANALPAC WL" in line:
        manalpac_val = line.strip("\n").split(": ")[1]
    elif "MADONGAN WL" in line:
        madongan_val = line.strip("\n").split(": ")[1]
    #impacts
    elif "gilbert_impacts" in line:
        gilbert_imp = line.strip("\n").split(": ")[1]
    elif "sarrat_impacts" in line:
        sarrat_imp = line.strip("\n").split(": ")[1]
    elif "darasdas_impacts" in line:
        darasdas_imp = line.strip("\n").split(": ")[1]
    elif "tabtabagan_impacts" in line:
        tabtabagan_imp = line.strip("\n").split(": ")[1]
    elif "callusa_impacts" in line:
        callusa_imp = line.strip("\n").split(": ")[1]
    elif "manalpac_impacts" in line:
        manalpac_imp = line.strip("\n").split(": ")[1]
    elif "madongan_impacts" in line:
        madongan_imp = line.strip("\n").split(": ")[1]
    # extras
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
template_fileHF = open(str(current_dir) + "\\lrb_bulletin_template.qpt")
template_content = template_fileHF.read()
template_fileHF.close()
documentHF.setContent(template_content)


## load layout from template and add to Layout Manager
layoutHF.loadFromTemplate(documentHF, QgsReadWriteContext()) 
project.layoutManager().addLayout(layoutHF)


layoutHF = QgsProject.instance().layoutManager().layoutByName("lbulletin")

#layoutITEMS
station_status_img = layoutHF.itemById("lrb_map")
fb_number = layoutHF.itemById("fb_no")
weather_system = layoutHF.itemById("weather_system")
ave_rainfall = layoutHF.itemById("ave_rainfall")
fcst_rainfall = layoutHF.itemById("fcst_rainfall")
dam_gate_opening = layoutHF.itemById("dam_gate_opening")
issuance_date = layoutHF.itemById("issuance_date")
valid_until = layoutHF.itemById("valid_until")

fthreat = layoutHF.itemById("fthreat")
fthreat_tg = layoutHF.itemById("fthreat_tg")

gilbert_wl_val = layoutHF.itemById("gilbert_wl_val")
sarrat_wl_val = layoutHF.itemById("sarrat_wl_val")
darasdas_wl_val = layoutHF.itemById("darasdas_wl_val")
tabtabagan_wl_val = layoutHF.itemById("tabtabagan_wl_val")
callusa_wl_val = layoutHF.itemById("callusa_wl_val")
manalpac_wl_val = layoutHF.itemById("manalpac_wl_val")
madongan_wl_val = layoutHF.itemById("madongan_wl_val")

impact_gilbert = layoutHF.itemById("impact_gilbert")
impact_sarrat = layoutHF.itemById("impact_sarrat")
impact_darasdas = layoutHF.itemById("impact_darasdas")
impact_tabtabagan = layoutHF.itemById("impact_tabtabagan")
impact_callusa = layoutHF.itemById("impact_callusa")
impact_manalpac = layoutHF.itemById("impact_manalpac")
impact_madongan = layoutHF.itemById("impact_madongan")

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
issuance_date.setText(issuance)
valid_until.setText(validity)

gilbert_wl_val.setText(gilbert_val)
sarrat_wl_val.setText(sarrat_val)
darasdas_wl_val.setText(darasdas_val)
tabtabagan_wl_val.setText(tabtabagan_val)
callusa_wl_val.setText(callusa_val)
manalpac_wl_val.setText(manalpac_val)
madongan_wl_val.setText(madongan_val)

x_fcolor2(wl_gilbert_stat,gilbert_wl_val)
x_stat_bgcolor(wl_gilbert_stat,gilbert_wl_val)

x_fcolor2(wl_sarrat_stat,sarrat_wl_val)
x_stat_bgcolor(wl_sarrat_stat,sarrat_wl_val)

x_fcolor2(wl_darasdas_stat,darasdas_wl_val)
x_stat_bgcolor(wl_darasdas_stat,darasdas_wl_val)

x_fcolor2(wl_tabtabagan_stat,tabtabagan_wl_val)
x_stat_bgcolor(wl_tabtabagan_stat,tabtabagan_wl_val)

x_fcolor2(wl_callusa_stat,callusa_wl_val)
x_stat_bgcolor(wl_callusa_stat,callusa_wl_val)

x_fcolor2(wl_manalpac_stat,manalpac_wl_val)
x_stat_bgcolor(wl_manalpac_stat,manalpac_wl_val)

x_fcolor2(wl_madongan_stat,madongan_wl_val)
x_stat_bgcolor(wl_madongan_stat,madongan_wl_val)

impact_gilbert.setText(gilbert_imp)
text_format.setSize(adjust_fsize(gilbert_imp))
impact_gilbert.setTextFormat(text_format)

impact_sarrat.setText(sarrat_imp)
text_format.setSize(adjust_fsize(sarrat_imp))
impact_sarrat.setTextFormat(text_format)

impact_darasdas.setText(darasdas_imp)
text_format.setSize(adjust_fsize(darasdas_imp))
impact_darasdas.setTextFormat(text_format)

impact_tabtabagan.setText(tabtabagan_imp)
text_format.setSize(adjust_fsize(tabtabagan_imp))
impact_tabtabagan.setTextFormat(text_format)

impact_callusa.setText(callusa_imp)
text_format.setSize(adjust_fsize(callusa_imp))
impact_callusa.setTextFormat(text_format)

impact_manalpac.setText(manalpac_imp)
text_format.setSize(adjust_fsize(manalpac_imp))
impact_manalpac.setTextFormat(text_format)

impact_madongan.setText(madongan_imp)
text_format.setSize(adjust_fsize(madongan_imp))
impact_madongan.setTextFormat(text_format)

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


folder_path = str(current_dir) + "\\out\\svg\\"
filename = str(today) + "-laoag_data.svg"


station_status_img.setPicturePath(folder_path + filename)
#station_status_img.refreshPicture()

svg_path2 = os.path.join(str(current_dir) + "\\out2\\svg", str(today) + "-lrb_data.svg")
png_path2 = os.path.join(str(current_dir) + "\\out2\\png", str(today) + "-lrb_data.png")
pdf_path2 = os.path.join(str(current_dir) + "\\out2\\pdf", str(today) + "-lrb_data.pdf")


exporter = QgsLayoutExporter(layoutHF)
exporter.exportToSvg(svg_path2, QgsLayoutExporter.SvgExportSettings())
exporter.exportToImage(png_path2, QgsLayoutExporter.ImageExportSettings())
exporter.exportToPdf(pdf_path2, QgsLayoutExporter.PdfExportSettings())


print("DONE BULLETIN  DONE BULLETIN  DONE BULLETIN  DONE BULLETIN  DONE BULLETIN")


qgs.exitQgis()

#########################################################
