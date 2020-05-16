
from flask import Blueprint, views, render_template, make_response
from utils.captcha import Captcha
from io import BytesIO
from exts import alidayu

bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'img/png'
    return resp


class SignupView(views.MethodView):

    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        pass


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))