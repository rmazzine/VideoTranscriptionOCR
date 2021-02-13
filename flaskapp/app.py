import sys
sys.path.append('../')  # Must have a best solution

from flask import Flask
from flask_restful import Api

from flaskapp.routes.extract_video import ExtractVideo

app = Flask(__name__)

api = Api(app)

api.add_resource(ExtractVideo, '/extract_video')
