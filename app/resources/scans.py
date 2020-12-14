import threading
from datetime import datetime

from flask import current_app
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from flasgger import swag_from

from app.libs.get_host_port_arguments import get_host_port_arguments
from app.libs.check_host_and_port import check_host_and_port
from app.models.scanModel import ScanModel
from app.models.reportModel import ReportModel
from app.libs.nmapScan_threading import nmapScan_threading

resource_fields_id = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'status': fields.Boolean,
    'create_time': fields.DateTime,
    'finish_time': fields.DateTime
}

resource_fields_scanned = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'create_time': fields.DateTime,
    'finish_time': fields.DateTime
}

resource_fields_scanning = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'create_time': fields.DateTime
}

class Scans(Resource):
    def __init__(self):
        mode_choices     = ('intense', 'intense_udp', 'intense_all_tcp', 'intense_no_ping', 'ping', 'quick', 'quick_plus', 'quick_trace', 'regular', 'slow_comp')
        tcp_choices      = ('ACK', 'FIN', 'Maimon', 'Null', 'SYN', 'Connect', 'Window', 'Xmas')
        nontcp_choices   = ('UDP', 'IP', 'List', 'Ping', 'SCTP INIT', 'SCTP COOKIE-ECHO')
        timemode_choices = ('-T0', '-T1', '-T2', '-T3', '-T4', '-T5')

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host',      type = str, location = 'json', required = True, help = 'No host provided')
        self.reqparse.add_argument('port',      type = str, location = 'json')
        self.reqparse.add_argument('mode',      type = str, location = 'json', choices=mode_choices)
        self.reqparse.add_argument('tcp',       type = str, location = 'json', choices=tcp_choices)
        self.reqparse.add_argument('nontcp',    type = str, location = 'json', choices=nontcp_choices)
        self.reqparse.add_argument('timemode',  type = str, location = 'json', choices=timemode_choices)
        self.reqparse.add_argument('scan',      type = str, location = 'json')
        self.reqparse.add_argument('ping',      type = str, location = 'json')
        self.reqparse.add_argument('script',    type = str, location = 'json')
        self.reqparse.add_argument('target',    type = str, location = 'json')
        self.reqparse.add_argument('source',    type = str, location = 'json')
        self.reqparse.add_argument('other',     type = str, location = 'json')
        self.reqparse.add_argument('timing',    type = str, location = 'json')
        
        super(Scans, self).__init__()


    def post(self):
        """
        file: specs/scans_post.yml
        """
        args = self.reqparse.parse_args()
        args2 = dict(args)

        # check host and port
        code, message = check_host_and_port(args)
        if (code == 200):
            # host and port are right
            host, port, arguments = get_host_port_arguments(args2)
            create_time = datetime.now()
            scan = ScanModel(host=host, port=port, arguments=arguments, status=0, create_time=create_time, finish_time=create_time)

            scan.add_to_db()
            scan_id = scan.id

            # start a new threading to scan
            app_threading = current_app._get_current_object()
            t = threading.Thread(target=nmapScan_threading, args=(app_threading, host, port, arguments, scan_id))
            t.start()

            return {'scan_id': scan_id}, 200
        else:
            return {'message':message }, code


class ScanId(Resource):

    @marshal_with(resource_fields_id, envelope='resource')
    @swag_from('specs/scans_get_scanid.yml')
    def get(self, id):
        scan = ScanModel.find_by_id(id)
        if scan is not None:
            return scan
        else:
            return {'message':'scan id not exists.'}, 400

    @swag_from('specs/scans_delete_scanid.yml')
    def delete(self, id):
        scan = ScanModel.find_by_id(id)
        if scan is not None:
            # delete scan
            ScanModel.delete_by_id(id)
            # delete reports
            ReportModel.delete_by_id(id)

            return {'message':'ok.'}, 200
        else:
            return {'message':'scan id not exists.'}, 400


class Scanning(Resource):
    # return all scanning item
    @marshal_with(resource_fields_scanning, envelope='resource')
    @swag_from('specs/scans_scanning.yml')
    def get(self):
        scans = ScanModel.find_by_status(0)
        return scans


class Scanned(Resource):
    # 10 default, user can input the number
    # number must be > 0
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('limit', type=int, location='args')

        super(Scanned, self).__init__()

    @marshal_with(resource_fields_scanned, envelope='resource')
    @swag_from('specs/scans_scanned.yml')
    def get(self):
        args = self.reqparse.parse_args()

        if args.limit is not None:
            if args.limit <= 0:
                return {'message':'limit must > 0 '}, 400
            else:
                scans = ScanModel.find_by_status(1, args.limit)
        else:
            scans = ScanModel.find_by_status(1, 10)

        if scans is not None:
            return scans
        else:
            return {'message': 'no scanned scan'}, 400


class ScanTest(Resource):
    def get(self):
        ScanModel.update_status_finish_time(100)
        return {'message': 'test'}, 400
