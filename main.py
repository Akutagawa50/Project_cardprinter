import os

# PDF関係
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# .ini関係
import configparser

# Time 
import datetime

# GUI関係
import io
import PySimpleGUI as sg
from PIL import Image, ImageTk

# .iniを読み込む
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

def get_img_data(f, maxsize=(300, 300), first=False):
    """Generate image data using PIL
    """
    #print("open file:", f)
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

# 123x456 を 123, 456 に変換する関数
def get_size(size_str):
    x_index = size_str.find('x')
    if x_index == -1:
        return -1,-1
    a = int(size_str[:x_index])
    b = int(size_str[x_index+1:])
    return a,b

# PDFに画像を挿入する関数
def insert_img(pdf, img_path, img_size, locate, sheet_size=(210,297)): #pdf, 画像パス，カードの種類，カード中心x座標，カード中心y座標
    #pdf.drawInlineImage(img_path, locate[0]*mm, (sheet_size[1]-img_size[1]-locate[1])*mm, img_size[0]*mm, img_size[1]*mm)
    pdf.drawInlineImage(img_path, (locate[0]-img_size[0]/2)*mm, (sheet_size[1]-locate[1]-img_size[1]/2)*mm, img_size[0]*mm, img_size[1]*mm)

def make_pdf(img_paths, img_size, pdf = None,sheet_size = (210, 297), margin = (10,10), filename = 'img_printer.pdf'):
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
            img_locate.append((margin[0]+img_size[0]/2+i*(img_size[0]+img_margin[0]), (margin[1]+img_size[1]/2+j*(img_size[1]+img_margin[1]))))

    # PDFを生成
    if pdf == None:
        pdf = canvas.Canvas(filename, (sheet_size[0]*mm, sheet_size[1]*mm))    
        pdf.setTitle('img Printer')
        pdf.saveState()    # セーブ

    # 画像挿入
    i=0
    page = 0
    all_num = int(img_num[0]*img_num[1])
    for img_path in img_paths:
        if i // all_num > page:
            page += 1
            pdf.showPage()
        insert_img(pdf, img_path, img_size, img_locate[i % all_num])
        i += 1
    pdf.save()
    return pdf

_null_img_path = [os.getcwd(), 'imgs', 'null.png']
null_img_path = os.path.join(*_null_img_path)
_error_img_path = [os.getcwd(), 'imgs', 'error.png']
error_img_path = os.path.join(*_error_img_path)
print(null_img_path+'\n'+error_img_path)
layout = [\
    [sg.Text('用紙サイズ'), sg.Combo(list(config['sheet_size'].keys()), default_value='a4',size=(25, 1), key='sheet_pulldown', readonly=True)],\
    [sg.Text('カード種類'), sg.Combo(list(config['img_size'].keys()), default_value='duel_masters_ka-nabell',size=(25, 1), key='img_pulldown', readonly=True)],\
    [sg.Text('No 1', key = 'img_no', font = 20)],\
    [sg.Text('画像'), sg.InputText(key = 'img_path', size = (25,1), enable_events=True, readonly=True),\
        sg.FileBrowse(key="file1", initial_folder = config['file']['browse_dir'], file_types=(('jpegファイル', '*.jpg'), ('pngファイル', '*.png'),))],\
    [sg.Text('枚数'), sg.Combo(list(range(1,11)), default_value=0, size=(25, 1), key='imgnum_pulldown', enable_events=True, readonly=True)],\
    [sg.Image(data = get_img_data(null_img_path, first=True), key = 'image_display')],\
    [sg.Text('PDFファイル名'), sg.Input('img_printer',size=(27, 1), key='PDF_filename')],\
    [sg.Button('＜'), sg.Button('＞')],\
    [sg.Button('PDF化'), sg.Button('クリア'), sg.Button('すべてクリア'), sg.Button('終了')],\
    [sg.Text('', key='message')]]

window = sg.Window('Image Printer',layout, size = (350,600))

# イベントループ
img_no = 0
img_paths = []
img_num = []
while True:
    event, values = window.read()
    #print(event, values)
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'クリア':
        window['sheet_pulldown'].update('a4')
        window['img_pulldown'].update('duel_masters_ka-nabell')
        window['PDF_filename'].update('img_printer')
        window['message'].update('')
        try:
            img_paths.pop(img_no)
            img_num.pop(img_no)
            window['image_display'].Update(data = get_img_data(img_paths[img_no]))
            window['img_path'].update(img_paths[img_no])
            window['imgnum_pulldown'].update(img_num[img_no]) 
            #window['imgnum_pulldown'].Update(value = '1') 
        except:
            window['image_display'].Update(data = get_img_data(null_img_path))
            window['img_path'].update('')
            window['imgnum_pulldown'].update(0)


    elif event == 'すべてクリア':
        window['sheet_pulldown'].update('a4')
        window['img_pulldown'].update('duel_masters_ka-nabell')
        window['img_path'].update('')
        window['imgnum_pulldown'].update(0)
        window['image_display'].Update(data = get_img_data(null_img_path))
        window['img_no'].update('No 1')
        window['PDF_filename'].update('img_printer')
        window['message'].update('すべてクリアしました')
        img_no = 0
        img_paths = []
        img_num = []
            
    elif event == '＞':
        window['message'].update('')
        if len(img_paths) > img_no:
            img_no += 1
            window['img_no'].update('No ' + str(img_no+1))
            try:
                window['image_display'].Update(data = get_img_data(img_paths[img_no]))
                window['imgnum_pulldown'].update(img_num[img_no])
                window['img_path'].update(img_paths[img_no])
                #window['imgnum_pulldown'].Update(value = '1') 
            except:
                window['image_display'].Update(data = get_img_data(null_img_path))
                window['sheet_pulldown'].update('a4')
                window['img_pulldown'].update('duel_masters_ka-nabell')
                window['img_path'].update('')
                window['imgnum_pulldown'].update(0)
                window['image_display'].Update(data = get_img_data(null_img_path))

        
    elif event == '＜':
        window['message'].update('')
        if img_no > 0:
            img_no -= 1
            window['image_display'].Update(data = get_img_data(img_paths[img_no]))
            window['imgnum_pulldown'].update(img_num[img_no])
            window['img_no'].update('No ' + str(img_no+1))
            window['img_path'].update(img_paths[img_no])
            #window['imgnum_pulldown'].Update(value = '1') 

    elif event == 'img_path':
        window['message'].update('')
        try:
            window['image_display'].Update(data = get_img_data(values['img_path']))
            window['imgnum_pulldown'].Update(value = '1')
            if len(img_paths) > 0 and len(img_paths) > img_no: 
                img_paths[img_no] = values['img_path']
                img_num[img_no] = 1
            else:
                img_paths.append(values['img_path'])
                img_num.append(1)
        except:
            window['image_display'].Update(data = get_img_data(error_img_path))
            window['imgnum_pulldown'].Update(value = '0')
    
    elif event == 'imgnum_pulldown':
        window['message'].update('')
        try:
            img_num[img_no] = int(values['imgnum_pulldown'])
        except:
            window['imgnum_pulldown'].Update(0)
    
    elif event == 'PDF化':
        if len(img_paths) == 0:
            window['message'].update('PDF化できる画像がありません')
        else:
            print_imgs = []
            for i in range(len(img_paths)):
                for j in range(img_num[i]):
                    print_imgs.append(img_paths[i])
            img_size = get_size(config['img_size'][values['img_pulldown']])
            sheet_size= get_size(config['sheet_size'][values['sheet_pulldown']])
            if values['PDF_filename'] == 'img_printer':
                dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                filename = os.path.join(config['file']['download_dir'], 'img_printer_' + dt_now + '.pdf')
            else:
                filename = os.path.join(config['file']['download_dir'] , values['PDF_filename'] + '.pdf')
            make_pdf(img_paths=print_imgs, img_size = img_size, sheet_size = sheet_size, margin=(5,5), filename = filename)
            window['message'].update('PDF化しました')
            window['sheet_pulldown'].update('a4')
            window['img_pulldown'].update('duel_masters_ka-nabell')
            window['img_path'].update('')
            window['imgnum_pulldown'].update(0)
            window['image_display'].Update(data = get_img_data(null_img_path))
            window['img_no'].update('No 1')
            window['PDF_filename'].update('img_printer')
            img_no = 0
            img_paths = []
            img_num = []
