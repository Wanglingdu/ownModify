# coding:utf-8
from app import app
import time, pdb
import os
import re
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import datetime
import urllib
import json
import hashlib

def rop_detect(dest_dir, infos):
    start_time = time.time()
    img_name = set()
    for filename in os.listdir(dest_dir):
        if os.path.splitext(filename)[1].lower() == '.jpg' or \
                        os.path.splitext(filename)[1].lower() == '.png':
            img_name.add(filename)
    img_num = len(img_name)
    all_imgs = [0] * img_num
    size = (352, 264)
    loc_x = 50
    loc_y = 360
    background = Image.open(app.config['BACKGROUND'])
    num = 0
    for i, filename in enumerate(img_name):
        # im_np = cv2.imread(app.config['UPLOADED_PATH']+"/"+ filename)
        # im_np = cv2.resize(im_np, (0,0), fx=0.2, fy=0.2)
        # all_imgs[i] = np.copy(im_np)
        # shutil.move(app.config['UPLOADED_PATH']+"/"+ filename, dest_dir+"/"+filename)
        im = Image.open(dest_dir + "/" + filename)
        # im1 = im.resize((320, 240), Image.ANTIALIAS)
        # im_np = np.asarray(im1, dtype='float32')
        # print(im_np.shape)
        # Use newaxis object to create an axis of length one
        # all_imgs[i] = np.copy(im_np)
        im = im.resize(size, Image.ANTIALIAS)
        # print(im)
        # print(im)
        if num < 9:
            background.paste(im, (loc_x, loc_y, loc_x + size[0], loc_y + size[1]))
            loc_x = loc_x + size[0] + 20
        num += 1
        if num % 3 == 0:
            loc_x = 50
            loc_y = loc_y + size[1] + 40
    close_time = time.time()
    print("img process before:" + str(close_time - start_time))


    start_time = time.time()
    request_url = app.config["ROP_SERVICE"]
    msg_key = 'msg'
    # input_list = [input_data.tolist() for input_data in all_imgs]

    # input_list_json = json.dumps(input_list)
    dest_dir = re.sub('/milab', '', dest_dir)
    input_data = {'data_folder': dest_dir}
    print('________________________dest_dir:' + dest_dir)
    req = urllib.request.Request(url=request_url, data=urllib.parse.urlencode(input_data).encode("utf-8"))
    res_data = urllib.request.urlopen(req)
    close_time = time.time()
    print("detect service:" + str(close_time - start_time))

    start_time = time.time()
    res_dict = eval(res_data.read())
    print("____________________________________res_dict['code']:" + str(res_dict['code']))
    if int(res_dict['code']) == 1:
        if res_dict['diagnose'] == 'normal':
            pred_result = "正常"
            confidence_0 = res_dict['y_rop_normal'][0]
            confidence_1 = res_dict['y_rop_normal'][1]
        else:
            if res_dict['diagnose'] == "stage2":
                pred_result = "ROP 1/2期"
            else:
                pred_result = "ROP 3/4/5期"
            confidence = res_dict['y_rop_normal'][0]
            confidence_0 = res_dict['y_rop_normal'][1]
            confidence_2 = res_dict['y_stage_2_3'][0]
            confidence_3 = res_dict['y_stage_2_3'][1]
    else:
        pred_result = res_dict[msg_key]
        # try:
        #    print( ImageFont.truetype("static/fonts/msyhLight_1.0.ttc",45));
        # except:
        #    print( ImageFont.truetype("msyhLight_1.0.ttc",45));
    ttfont = ImageFont.truetype("/usr/share/fonts/type2/wqy-microhei.ttc", 36)
    # ttfont = ImageFont.truetype("uming.ttc",45)
    # ttfont = None
    draw = ImageDraw.Draw(background)
    draw.text((50, 50), u'姓名: ' + infos['name'], fill=(0,0,0), font=ttfont)
    if infos['date']:
        draw.text((450, 50), u'检查日期: ' + infos['date'].strftime('%Y-%m-%d %H:%M:%S'), fill=(0, 0, 0), font=ttfont)
    else:
        draw.text((450, 50), u'检查日期:', fill=(0, 0, 0), font=ttfont)
    draw.text((1000, 50), u'眼: ' + infos['RL'], fill=(0, 0, 0), font=ttfont)
    draw.text((50, 1280), u'诊断意见 :' + pred_result, fill=(0, 0, 0), font=ttfont)
    draw.text((100, 1370), u'类型', fill=(0, 0, 0), font=ttfont)
    draw.text((100, 1500), u'置信度', fill=(0, 0, 0), font=ttfont)
    if res_dict['diagnose'] == 'normal':
        draw.text((300, 1370), u'正常', fill=(0, 0, 0), font=ttfont)
        draw.text((500, 1370), u'ROP', fill=(0, 0, 0), font=ttfont)
        draw.text((300, 1500), u'%.2f%%' % (confidence_0 * 100.), fill=(0, 0, 0), font=ttfont)
        draw.text((500, 1500), u'%.2f%%' % (confidence_1 * 100.), fill=(0, 0, 0), font=ttfont)
    else:
        print(confidence, confidence_2, confidence_3, confidence_2 * confidence * 100., str(confidence),
              str(confidence)[:6])
        draw.text((300, 1370), u'正常', fill=(0, 0, 0), font=ttfont)
        draw.text((500, 1370), u'ROP 1/2期', fill=(0, 0, 0), font=ttfont)
        draw.text((750, 1370), u'ROP 3/4/5期', fill=(0, 0, 0), font=ttfont)
        draw.text((300, 1500), u'%.2f%%' % (confidence * 100.), fill=(0, 0, 0), font=ttfont)
        draw.text((500, 1500), u'%.2f%%' % (confidence_2 * confidence_0 * 100.), fill=(0, 0, 0), font=ttfont)
        draw.text((750, 1500), u'%.2f%%' % (confidence_3 * confidence_0 * 100.), fill=(0, 0, 0), font=ttfont)
    filename = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:20]
    while(os.path.exists(os.path.join(app.config['REPORT'], filename + '.jpg'))):
        filename = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:20]
    background.save(app.config['REPORT'] + '/' + filename + '.jpg')
    img_name.clear()
    close_time = time.time()
    print("draw result:" + str(close_time - start_time))
    return pred_result, filename
