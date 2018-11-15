# coding:utf-8
import os, pdb
import re
import datetime
from flask import session
import shutil
from .detect import rop_detect
from ..models import BcInfo
from app import app, db

img_format = ['.png','.jpg','.jpeg']

def get_info(filename, path):
    info = dict()
    with open(
        os.path.join(path, filename), 'r', encoding='utf-8'
    ) as f:
        content = f.read()
        ok = 1
        try:
            m = re.search('Name:.*', content)
            info['name'] = re.sub('(Name:)|[,\n]', '', m.group(0)).strip()
        except:
            ok = 0
            info['name'] = 'unknown'

        try:
            m = re.search('Started:.*', content)
            date = re.sub('(Started:)|[,\n]', '', m.group(0)).strip()
            info['date'] = datetime.datetime.strptime(date, '%A %B %d %Y %I:%M:%S %p')
        except:
            info['date'] = None

    return info, ok


def get_RL(filename, path):
    info = dict()
    with open(
        os.path.join(path, filename), 'r', encoding='utf-8'
    ) as f:
        content = f.read()
        try:
            m = re.search('SessionItem.ImageOf=.*', content)
            info['RL'] = re.sub('SessionItem.ImageOf=|[\n]', '', m.group(0)).strip()
        except:
            info['RL'] = None
    return info


def database_insert(path, record, RL):
    #pdb.set_trace()
    record['path'] = os.path.join(path, RL)
    record['RL'] = RL
    #try:
        #record['model_result'], record['report'] = ('ROP 2期',
        #                                            'eb52cfc5e5b139aa971f6c9b52aa228f_zx0268361_20161122_OD')
    print(record['path'])
    record['model_result'], record['report'] = rop_detect(record['path'], record)
    #except:
    #    print('model inspect error:no such path or no photo in path')
    record['username'] = session['USERNAME']
    record['doctor_result'] = ''

    info = Rop_info(path=record['path'],
                    patient_name=record['name'],
                    date=record['date'],
                    model_result=record['model_result'],
                    username=record['username'],
                    doctor_result=record['doctor_result'],
                    upload_time=datetime.datetime.now(),
                    rl=RL,
                    foldername=record['report'])
    db.session.add(info)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print('数据插入失败')
    return record


def insert_rop_data(path):
    record= dict()
    print('__________________________path:' + path)
    img_name = dict()
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1].lower() in img_format:
            img_name[os.path.splitext(filename)[0]] = filename
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == '.txt':
            info = get_RL(filename, path)
            if info['RL']:
                lpath = os.path.join(path, info['RL'])
                if not os.path.exists(lpath):
                    os.mkdir(lpath)
                shutil.move(
                    os.path.join(path, filename),
                    os.path.join(lpath, filename)
                )
                try:
                    shutil.move(
                        os.path.join(path, img_name[os.path.splitext(filename)[0]]),
                        os.path.join(lpath, img_name[os.path.splitext(filename)[0]])
                    )
                except Exception as e:
                    print(e.message)
            else:
                print('not distinguish eyes photo')
    img_name.clear()
    for filename in os.listdir(os.path.join(path, 'OD')):
        if os.path.splitext(filename)[1] == '.txt':
            record, ok = get_info(filename, os.path.join(path, 'OD'))
            if ok == 1:
                break
    if ok == 0:
        record['name'] = 'unknown'
        record['date'] = None
    if os.path.exists(path+'/OD'):
        database_insert(path, record, 'OD')
    if os.path.exists(path+'/OS'):
        database_insert(path, record, 'OS')
