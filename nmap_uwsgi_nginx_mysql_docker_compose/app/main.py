import os
import sys
from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from app.libs.database import db
from app.resources.scans import Scans
from app.resources.scans import ScanId
from app.resources.scans import Scanning
from app.resources.scans import Scanned
from app.resources.scans import ScanTest
from app.resources.reports import Reports
from app.resources.scripts import Scripts
from app.resources.scripts import ScriptsDir



app = Flask(__name__)

# mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nmapuser:123456@mysql:3306/nmap'

# sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'nmapuser'),
    os.getenv('DB_PASSWORD', '123456'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'nmap')
)



db.init_app(app)

with app.app_context():
    #db.drop_all()
    db.create_all()

api = Api(app, catch_all_404s=True)
swagger = Swagger(app)
# add resources
api.add_resource(Scans, '/v1.0/scans')
api.add_resource(ScanId, '/v1.0/scans/<int:id>')
api.add_resource(Scanning, '/v1.0/scans/scanning')
api.add_resource(Scanned, '/v1.0/scans/scanned')
api.add_resource(ScanTest, '/v1.0/scans/scantest')

api.add_resource(Reports, '/v1.0/reports/<int:id>')
api.add_resource(Scripts, '/v1.0/scripts/')
api.add_resource(ScriptsDir, '/v1.0/scripts/dir')


