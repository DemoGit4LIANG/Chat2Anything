from io import BytesIO

from flask import session, make_response

from applications.common.utils.gen_captcha import vieCode


# 生成验证码
def get_captcha():
    image, code = vieCode().GetCodeImage()
    code = ''.join(code).lower()
    out = BytesIO()
    session["code"] = code
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp, code