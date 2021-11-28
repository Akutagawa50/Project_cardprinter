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

def insert_card(img_path, card_kind, x, y): #画像パス，カードの種類，x座標，y座標
    width, height = get_size(config_ini['card_size'][card_kind])
    pdf.drawInlineImage(img_path, x*mm, (sheet_size_y-height-y)*mm,width*mm, height*mm)
    #pdf.restoreState()

imgs_path = ['./imgs/1.jpg', './imgs/2.jpg', './imgs/3.jpg']
width, height = get_size(config_ini['card_size']['duel_masters'])
card_kind = 'duel_masters_ka-nabell'
for i in range(3):
    insert_card(imgs_path[0], card_kind, 5, i*(height+5)+5)
    insert_card(imgs_path[1], card_kind, (sheet_size_x-width)/2.0, i*(height+5)+5)
    insert_card(imgs_path[2], card_kind, (sheet_size_x-width)-5, i*(height+5)+5)

pdf.showPage()
insert_card(imgs_path[0], card_kind, 5, 5)
insert_card(imgs_path[1], card_kind, (sheet_size_x-width)/2.0, 5)
insert_card(imgs_path[2], card_kind, (sheet_size_x-width)-5, 5)


#insert_card('./imgs/erase.png', 'duel_masters', (sheet_size_x-width)/4.0, (sheet_size_y-height)/2.0)

pdf.save()
