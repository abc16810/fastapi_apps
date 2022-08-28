import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# redis
access_token = "access_token"
CAPTCHA_ID = "captcha:{captcha_id}"
LOGIN_ERROR_TIMES = "login_error_times:{ip}"
LOGIN_USER = "login_user:{token}"
LOGIN_PATH = "/login"
LOGOUT_PATH = "/logout"