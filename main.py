import os
import sys
import time
import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory
from PIL import Image
from pathlib import Path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def apply_logo(path:str, image_name:str, logo_number, resize_multi:float = 0.1):
    input_image = Image.open(path + '/' + image_name)
    resized_width = input_image.size[0]*resize_multi
    
    logo = Image.open(resource_path('logo{}.png'.format(str(logo_number)))).resize((
            int(resized_width+(resized_width*0.2)),
            int(resized_width/input_image.size[0]*input_image.size[1])
        )
    )

    input_image.paste(logo, (
        input_image.size[0] - int(logo.size[0]*1.1), 
        input_image.size[1] - int(logo.size[1]*1.1)
    ), logo)

    pn = str(Path(__file__).parent.parent.parent.resolve()) + '/output'
    if not os.path.exists(pn):
        os.makedirs(pn)
    input_image.save('{}/{}'.format(
        pn,
        str().join(image_name.split('.')[:-1]) + '.JPEG'
    ), 'JPEG')

def progressBar(current:float, total, barLength = 25):
    percent = current * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print(
        ('Progress: [%s%s] %d %%' % (arrow, spaces, percent)) + 
        '(finished ' + str(current) + ' out of ' + str(total) + ')', end='\r')

Tk().withdraw()
path = askdirectory()
n,st = 1,time.time()

errorLog = {}

print('\n')
print('Process started! Watermarking all images from path: " ' + str(path) + ' "')
for image in os.listdir(path):
    try:
        apply_logo(path, image, 2, 0.1)

        progressBar(n, len(os.listdir(path)))
        n += 1
    except Exception as e:
        errorLog[image] = e

print(
    'Process completed! Elapsed: ' + 
    str(int(time.time()-st)) + ' seconds or ' 
    + str((time.time()-st)/len(os.listdir(path))) + ' per image, at ' 
    + str(datetime.datetime.now())
)

if errorLog != {}:
    print('\n\nHowever, some images were not able to be processed:\n')
    for error in errorLog:
        print(str(error) + ' : ' + str(errorLog.get(error)))