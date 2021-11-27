# PDF関係
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A3, B5, B4, portrait

# .ini関係
import configparser

# GUI関係
import PySimpleGUI as sg

# 123x456 を 123, 456 に変換する関数
def get_size(size_str):
    x_index = size_str.find('x')
    if x_index == -1:
        return -1,-1
    a = int(size_str[:x_index])
    b = int(size_str[x_index+1:])
    return a,b

sheet_all_kind={'A3':A3, 'A4':A4, 'B5':B5, 'B4':B4}

# .iniを読み込む
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

# PDFファイルを生成する ###
file_name = 'OFFICE54.pdf'    # ファイル名を設定
sheet_kind = "A4"

sheet_size_x = sheet_all_kind[sheet_kind][0]/mm
sheet_size_y = sheet_all_kind[sheet_kind][1]/mm

'''
print(sheet_all_kind[sheet_kind])
print(config_ini['sheet_size'][sheet_kind])
print(sheet_size_x, sheet_size_y)
print(mm)
'''

pdf = canvas.Canvas(file_name, portrait(sheet_all_kind[sheet_kind]))    # PDFを生成、サイズはA4
pdf.setTitle('Card Printe')
pdf.saveState()    # セーブ

def insert_card(img_path, card_kind):
    width, height = get_size(config_ini['card_size'][card_kind])
    #pdf.drawInlineImage(img_path, 0*mm, (sheet_size_y-0)*mm, width*mm, height*mm)
    pdf.drawInlineImage(img_path, (0)*mm, (sheet_size_y-height-0)*mm,width*mm, height*mm)
    pdf.restoreState()
    pdf.save()

insert_card('./imgs/towaryu.jpg', 'duel_masters_jumbo')
