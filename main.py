# PDF関係
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

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

# .iniを読み込む
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

# PDFファイルを生成する ###
file_name = 'card_printer.pdf'  # ファイル名を設定
sheet_kind = "A4"               # 用紙のサイズ

sheet_size_x, sheet_size_y = get_size(config_ini['sheet_size'][sheet_kind])

pdf = canvas.Canvas(file_name, (sheet_size_x*mm,sheet_size_y*mm))    # PDFを生成
pdf.setTitle('Card Printe')
pdf.saveState()    # セーブ

def insert_card(img_path, card_kind): #画像パス，カードの種類
    width, height = get_size(config_ini['card_size'][card_kind])
    pdf.drawInlineImage(img_path, (0)*mm, (sheet_size_y-height-0)*mm,width*mm, height*mm)
    pdf.restoreState()
    pdf.save()

insert_card('./imgs/towaryu.jpg', 'duel_masters')
