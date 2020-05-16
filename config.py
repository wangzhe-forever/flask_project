import os

DEBUG = True

SECRET_KEY = os.urandom(24)
# 数据库配置
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'flask_project'
DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 此为设置session里的user_id
CMS_USER_ID = 'ASAGAGR'

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False/465



# 阿里大于相关配置
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'D9E'
ALIDAYU_SIGN_NAME = 'FLASK论坛专用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'