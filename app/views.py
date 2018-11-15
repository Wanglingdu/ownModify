#coding=utf-8
from app import app, db
from .forms import LoginForm
from .models import User, BcInfo
from .utils import img_detector
from sqlalchemy import and_, or_
from flask import render_template, flash, redirect, request, url_for, g, session, jsonify

import numpy as np
import os,hashlib,json,datetime,time,cv2,urllib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    name = StringField('名字')
    
    
@app.route('/show/', methods=["GET", "POST"])
def lst_history():
    folder_path = './app/static/upload/report'
    local_service = 'http://192.168.7.239:6112'
    lst = os.listdir(folder_path)
    name  = []
    time  = []
    label = []
    queue = []
    for one in lst:
        example_inqueue = []
        example_inqueue.append(one[:-20])
        example_inqueue.append(one[-19:-4])
        path = local_service+ os.path.join(folder_path, one).split('app')[-1]
        example_inqueue.append(path)
        queue.append(example_inqueue)
    queue.sort(key=lambda x:x[1], reverse=True)
    length = len(queue)
    for i in range(length):
        name.append(queue[i][0])
        time.append(queue[i][1])
        label.append(queue[i][2])
    return render_template('show0.html')
    return render_template('show.html', name = name, time = time, label = label, length = length)
    return render_template('show.html')


def insert_bcinfo():
    record = {
        "username":session["username"],
        "upload_path":session["upload_path"],
        "upload_date":session["upload_date"],
        "model_result":session["model_result"],
        "doctor_result":'hello world',
        "report_path":session["report_path"]
    }
    bcinfo = BcInfo(**record)
    db.session.add(bcinfo)
    db.session.commit()

    
def generate_report(folder_path,save_path):
    generated_column = [36, 360]
    num_str_inline = 19
    length_str = 16
    height = 60 + 500 * 2 + 36
    width = 700
    channel = 3
    height_before_img = 60
    grid_height = 460
    grid_width = 304
    text_height = 40
    num_of_img = 4
    dict_img = {0:'LEFT_CC',
                1:'RIGHT_CC',
                2:'LEFT_MLO',
                3:'RIGHT_MLO'}
    
    lst_img = os.listdir(folder_path)
    lst_draw = [u'',u'',u'',u'']
    for img_name in lst_img:
        if u'LEFT_CC' in img_name:
            lst_draw[0] = img_name
        if u'RIGHT_CC' in img_name:
            lst_draw[1] = img_name
        if u'LEFT_MLO' in img_name:
            lst_draw[2] = img_name
        if u'RIGHT_MLO' in img_name:
            lst_draw[3] = img_name
    
    
    generated_report_np = np.ones((height, width, channel))
    generated_report_np = generated_report_np * 255 # draw white background



    # draw X image
    for i in range(num_of_img):
        minr = height_before_img + int(i/2)*(grid_height+text_height)
        minc = int(generated_column[i%2])
        maxr = int(minr + grid_height)
        maxc = int(minc + grid_width)
        img_name = os.path.join(folder_path, lst_draw[i])
        print (img_name)
        cv2.imread(img_name)
        reshaped_us = cv2.resize(cv2.imread(img_name),(grid_width, grid_height), interpolation=cv2.INTER_AREA)
        print (reshaped_us.shape)
        generated_report_np[minr:maxr,minc:maxc,:] = reshaped_us
    
    generated_dir = save_path+folder_path.split('/')[-1]+'.jpg'
    cv2.imwrite(generated_dir, generated_report_np, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return generated_dir
    
    
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    '''
    Load the index page.
    '''
    default_img = '/static/img/default.png'
    
    session["username"] = "milab"
    if request.method == "POST":
        f = []
        for i in range(len(request.files)):
            f.append(request.files.get('report'+str(i)))
        print (f)
        folder_name = ''
        for name in f:
            temp_name = name.filename.split('/')[-1]
            if '_LEFT_CC' in temp_name:
                temp_name = temp_name.split('.png')[0]
                date_and_time = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()+ 28800))
                folder_name = temp_name.replace('LEFT_CC',date_and_time)
        print (folder_name)
        if folder_name == '':
            print (default_img)
            return jsonify(url=default_img , is_t_pic = 0)
        
        
        folder_path = os.path.join(app.config['UPLOADED_PATH'], folder_name)
        os.makedirs(folder_path)
        for one_img in f:
            img_path = os.path.join(folder_path, one_img.filename.split('/')[-1])
            one_img.save(img_path)
       
        #session["cutted_img_list"] = cutted_img_list
        U_save_report_path = app.config['SAVE_REPORT_PATH']
        Ureport_path = generate_report(folder_path, U_save_report_path)
        session["upload_path"] = folder_path
        session["upload_date"] = datetime.datetime.now()
        
        print (Ureport_path)
        return jsonify(url=Ureport_path.lstrip('app/'), is_t_pic = 1)
    return render_template('index.html')

@app.route('/wechat', methods=["GET", "POST"])
def wechat():
    '''
    Load the mobile page.
    '''
    session["username"] = "milab"
    if request.method == "POST":
        f = request.files.get('reportImg')
        img_path = os.path.join(app.config['UPLOADED_PATH'], f.filename)
        date_and_time = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
        img_path = img_path.rstrip('.jpg')+"_"+date_and_time+".jpg"
        f.save(img_path)
        img = cv2.imread(img_path)
        frac = img.shape[1] / 800.0
        img_reshaped = cv2.resize(img,(int(img.shape[1]/frac), int(img.shape[0]/frac)), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img_path, img_reshaped, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        cutted_output_path = "app/static/upload/cutted"
        marked_output_path = "app/static/upload/marked"
        coordinates = img_detector.img_detector(img_path)
        cutted_img_list = img_detector.img_cutter(img_path, cutted_output_path, coordinates)
        marked_img_path = img_detector.img_marker(img_path, marked_output_path, coordinates)
        session["upload_path"] = img_path
        session["upload_date"] = datetime.datetime.now()
        session["cutted_img_list"] = cutted_img_list
        return jsonify(url=marked_img_path.lstrip('app/'))
    return render_template('index_wechat.html')

def post(url, data):
    data = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url=url, data=data)
    response = urllib.request.urlopen(request, data)
    return response.read()


@app.route('/MammogramDetect',methods=["GET"])
def MammogramDetect():
    request_url = app.config['DETECT_SERVICE']
    if request.method == "GET":
        filename = os.path.split(session["upload_path"])[-1]
        postdata = {"img_path":session["upload_path"]}
        response = post(request_url, postdata)
        response_str = str(response, encoding = "utf8")
        response_str = json.loads(response_str)
        report_path = response_str["report_path"]
        print (report_path)
        re_p = report_path.split('/app')[-1]
        print (re_p)
        return jsonify(report_path=re_p)
    return jsonify(res="Failed")


@app.route('/DeepBCDetect',methods=["GET"])
def DeepBCDetect():
    request_url = app.config['BC_SERVICE']
    if request.method == "GET":
        filename = os.path.split(session["upload_path"])[-1]
        postdata = {"img_path":session["upload_path"], "filename":filename}
        response = post(request_url, postdata)
        response = json.loads(response)
        code = response["code"]
        diagnosis = response["diagnosis"]
        print(diagnosis)
        report = np.array(response["report"])
        report_path = app.config['REPORT_PATH']+filename.rstrip('.jpg')+"_report.jpg"
        session["model_result"] = str(diagnosis)
        session["report_path"] = report_path
        cv2.imwrite(report_path, report, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        img_list = [path.lstrip('/app') for path in session["cutted_img_list"]]
        insert_bcinfo()
        return jsonify(diagnose=diagnosis,img_list=img_list,report_path=report_path.lstrip('/app'))
    return jsonify(res="Failed")
