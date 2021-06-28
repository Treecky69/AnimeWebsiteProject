from flask import Flask
from flask import *
#import AnimeWebsiteProject.views
app = Flask(__name__)
user = Blueprint("user", __name__)
admin = Blueprint("admin", __name__)