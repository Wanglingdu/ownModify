import os
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


#DataBase
SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@172.17.0.4:3306/deepbc'
#SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@127.0.0.1:3306/deepbc'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# Upload Image
UPLOADED_PATH = 'app/static/upload/upload_img/'
SAVE_REPORT_PATH = 'app/static/upload/Ureport/'
REPORT_PATH = 'app/static/upload/report/'
#BC_SERVICE = "http://172.17.0.5:5000/mxnet/breast_diagnosis_report"
DETECT_SERVICE = "http://192.168.7.239:6113/mxnet"
#BC_SERVICE = "http://192.168.7.178:7575/mxnet/breast_diagnosis_report"
