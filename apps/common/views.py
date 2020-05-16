
from flask import Blueprint, request
from exts import alidayu
from utils import restful
from utils.captcha import Captcha

bp = Blueprint("common", __name__, url_prefix="/c")


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    telephone = request.args.get('telephone')
    if not telephone:
        return restful.parmaserror(message='请传入手机号码!')
    captcha = Captcha.gene_text(number=4)
    if alidayu.send_sms(telephone, code=captcha):
        return restful.success()
    else:
        return restful.parmaserror(message='短信验证码发送失败!')