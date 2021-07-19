from flask import Flask
from pathlib import Path
import os
from flask_login import LoginManager

os_upload_path = os.path.join("static","uploads","images")
IMAGE_UPLOAD_DIR = Path(os_upload_path)

if not IMAGE_UPLOAD_DIR.exists():
    os.makedirs(os_upload_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key=b'bb5gb4grvsdf4ccecdrc\wq;dql[p,qckldcmdmdlmkv65d15123mm3oi'

login_manager=LoginManager()
login_manager.init_app(app)

login_manager.login_view="login"
login_manager.login_message=u"Iltimos login qiling!!!"
login_manager.login_message_category="danger"
