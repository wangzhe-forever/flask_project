
from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .models import CMSUser,CMSPermission
from .decorators import login_required, permission_required
import config
from exts import db, mail
from utils import restful, wzcache
from flask_mail import Message
import string
import random

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

#
# @bp.route('/email/')
# def send_email():
#     message = Message("邮件发送", recipients=["1377216268@qq.com"], body="测试")
#     mail.send(message)


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.parmaserror("请传递邮箱参数!")
    #验证码
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    # source.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    captcha = "".join(random.sample(source, 6))
    print(captcha)
    message = Message("Flask论坛邮箱验证码", recipients=[email], body="您的验证码是:%s" % captcha)
    try:
        mail.send(message)
    except:
        return restful.severerror()
    wzcache.set(email, captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONT_USER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMS_USER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


class LoginView(views.MethodView):
    # 这个装饰器没有生效后期要解决
    # decorators = [login_required()]

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱或者密码错误")
        else:
            print(form.errors)
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code": 200, "message": ""})
                return restful.success()
            else:
                return restful.parmaserror("旧密码错误!")
        else:
            return restful.parmaserror(form.get_error())


class ResetEmailView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.parmaserror()


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
