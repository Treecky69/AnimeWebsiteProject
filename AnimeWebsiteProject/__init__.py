from flask import Flask
from flask import *
#import AnimeWebsiteProject.views
app = Flask(__name__, static_folder=".\\looks\\static")
home_view = Blueprint("home_view", __name__, template_folder=".\\looks\\templates")
