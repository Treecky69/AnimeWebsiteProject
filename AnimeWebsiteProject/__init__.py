from flask import Flask
from flask import *
from sys import platform
#import AnimeWebsiteProject.views
app = Flask(__name__)
user = Blueprint("user", __name__)
if platform == "linux":
    admin = Blueprint("admin", __name__, template_folder="./templates/admin")
if platform == "win32":
    admin = Blueprint("admin", __name__, template_folder=".\\templates\\admin")