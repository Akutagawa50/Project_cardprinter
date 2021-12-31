# PDF関係
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# .ini関係
import configparser

# GUI関係
import PySimpleGUI as sg

# .iniを読み込む
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


# 123x456 を 123, 456 に変換する関数
def get_size(size_str):
    x_index = size_str.find('x')
    if x_index == -1:
        return -1,-1
    a = int(size_str[:x_index])
    b = int(size_str[x_index+1:])
    return a,b

# PDFに画像を挿入する関数
def insert_card(pdf, img_path, card_size, locate, sheet_size=(210,297)): #pdf, 画像パス，カードの種類，カード中心x座標，カード中心y座標
    #pdf.drawInlineImage(img_path, locate[0]*mm, (sheet_size[1]-card_size[1]-locate[1])*mm, card_size[0]*mm, card_size[1]*mm)
    pdf.drawInlineImage(img_path, (locate[0]-card_size[0]/2)*mm, (sheet_size[1]-locate[1]-card_size[1]/2)*mm, card_size[0]*mm, card_size[1]*mm)

def make_pdf(img_paths, img_size, sheet_size = (210, 297), margin = (10,10), filename = 'card_printer.pdf'):
    # 1ページ内に入る画像の数と画像間のマージンを計算
    img_num = []
    img_margin=[]
    for i in range(2):
        # 枚数を計算
        img_num.append(int(sheet_size[i]-2*margin[i]) // int(img_size[i]))
        
        # 余白を計算
        if img_num[i] == 1:
            # 0割り回避
            img_margin.append(0.0)
        else:
            img_margin.append(((sheet_size[i]-2*margin[i]) % img_size[i])/(img_num[i]-1))
    
    # 画像の配置場所の座標を計算
    img_locate = []
    for j in range(img_num[1]):
        for i in range(img_num[0]):
            # 画像が1枚のときは中央に配置
            if img_num[0] == 1 and img_num[1] == 1:
                img_locate.append((sheet_size[0]/2, sheet_size[1]/2))
                break
            # 縦横いずれかの画像が1枚のときの処理
            elif img_num[0] == 1:
                img_locate.append((sheet_size[0]/2, (margin[1]+img_size[1]/2+j*(img_size[1]+img_margin[1]))))
            elif img_num[1] == 1:
                img_locate.append((margin[0]+img_size[0]/2+i*(img_size[0]+img_margin[0]), sheet_size[1]/2))
            # 縦横の枚数がそれぞれ複数枚のとき
            else:
                img_locate.append((margin[0]+img_size[0]/2+i*(img_size[0]+img_margin[0]), (margin[1]+img_size[1]/2+j*(img_size[1]+img_margin[1]))))

    # PDFを生成
    pdf = canvas.Canvas(filename, (sheet_size[0]*mm, sheet_size[1]*mm))    
    pdf.setTitle('Card Printer')
    pdf.saveState()    # セーブ

    # 画像挿入
    i=0
    page = 0
    all_num = int(img_num[0]*img_num[1])
    for img_path in img_paths:
        if i // all_num > page:
            page += 1
            pdf.showPage()
        insert_card(pdf, img_path, img_size, img_locate[i % all_num])
        i += 1
    pdf.save()
    return pdf


layout = [[sg.Text('Card Printer')]]
input_key = []
pulldown_key = []
delete_key = []
for i in range(1,20,2):
    layout.append([sg.Text((str(i).rjust(2)+'枚目').rjust(4, '　')), sg.Input(key='input'+str(i)), \
        sg.Text('枚数', size=(4, 1)),sg.Combo(list(range(1,10)), default_value=1,size=(5, 1), key='pulldown'+str(i)), sg.Button('削除', key='delete'+str(i)),\
        sg.Text((str(i+1).rjust(2)+'枚目').rjust(4, '　')), sg.Input(key='input'+str(i+1)), \
        sg.Text('枚数', size=(4, 1)),sg.Combo(list(range(1,10)), default_value=1,size=(5, 1), key='pulldown'+str(i+1)), sg.Button('削除', key='delete'+str(i+1))])
    input_key.append('input'+str(i))
    input_key.append('input'+str(i+1))
    pulldown_key.append('pulldown'+str(i))
    pulldown_key.append('pulldown'+str(i+1))
    delete_key.append('delete'+str(i))
    delete_key.append('delete'+str(i+1))
layout.append([sg.Button('印刷'), sg.Button('クリア'), sg.Button('終了')])

window = sg.Window('画面を表示',layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'クリア':
        for key in input_key:
             window[key].update('')
        

# ファイル名を設定
filename = 'card_printer.pdf'

# 用紙のサイズ
sheet_kind = 'A4'

# カードの種類
card_kind = 'duel_masters_ka-nabell'

# 画像の場所
img_paths = ['./imgs/1.jpg', './imgs/2.jpg', './imgs/3.jpg', './imgs/1.jpg', './imgs/2.jpg', './imgs/3.jpg', './imgs/1.jpg', './imgs/2.jpg', './imgs/3.jpg', './imgs/1.jpg', './imgs/2.jpg', './imgs/3.jpg']

sheet_size= get_size(config['sheet_size'][sheet_kind])
card_size = get_size(config['card_size'][card_kind])

make_pdf(img_paths, card_size, sheet_size, margin=(5,5), filename = filename)
