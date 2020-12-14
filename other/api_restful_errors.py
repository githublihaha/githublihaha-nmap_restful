from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse
import nmap


nmaperrors = {
    'PortScannerError': {
        'status': 400,
        'message': "nmap PortScannerError"
    }
}


app = Flask(__name__)
api = Api(app, catch_all_404s=True, errors=nmaperrors)


class NmapReq(Resource):
    def __init__(self):
        mode_choices = ('intense', 'intense_udp', 'intense_all_tcp', 'intense_no_ping',
                        'ping', 'quick', 'quick_plus', 'quick_trace', 'regular', 'slow_comp')
        tcp_choices = ('-sA', '-sF', '-sM', '-sN', '-sS', '-sT', '-sW', '-sX')
        nontcp_choices = ('-sU', '-sO', '-sL', '-sn', '-sY', '-sZ')
        timemode_choices = ('-T0', '-T1', '-T2', '-T3', '-T4', '-T5')

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'host',      type=str, location='json', required=True, help='No host provided')
        self.reqparse.add_argument('port',      type=str, location='json')
        self.reqparse.add_argument(
            'mode',      type=str, location='json', choices=mode_choices)
        self.reqparse.add_argument(
            'tcp',       type=str, location='json', choices=tcp_choices)
        self.reqparse.add_argument(
            'nontcp',    type=str, location='json', choices=nontcp_choices)
        self.reqparse.add_argument(
            'timemode',  type=str, location='json', choices=timemode_choices)
        self.reqparse.add_argument('scan',      type=str, location='json')
        self.reqparse.add_argument('ping',      type=str, location='json')
        self.reqparse.add_argument('script',    type=str, location='json')
        self.reqparse.add_argument('target',    type=str, location='json')
        self.reqparse.add_argument('source',    type=str, location='json')
        self.reqparse.add_argument('other',     type=str, location='json')
        self.reqparse.add_argument('timing',    type=str, location='json')

        super(NmapReq, self).__init__()

    def post(self):
        # nmap scan
        args = self.reqparse.parse_args()
        result = nmapScan(args)

        return {'result':result}, 200

    def get(self):
        # get help, no paras
        help_message = {
            'host'    : 'string for hosts as nmap use it "scanme.nmap.org" or "198.116.0-255.1-127" or "216.163.128.20/20"',
            'port'    : 'string for ports as nmap use it "22,53,110,143-4564"',
            'mode'    : 'one of (intense, intense_udp, intense_all_tcp, intense_no_ping, ping, quick, quick_plus, quick_trace, regular, slow_comp)',
            'tcp'     : 'one of (-sA, -sF, -sM, -sN, -sS, -sT, -sW, -sX)',
            'nontcp'  : 'one of (-sU, -sO, -sL, -sn, -sY, -sZ)',
            'timemode': 'one of (-T0, -T1, -T2, -T3, -T4, -T5)',
            'scan'    : 'other scan parameters, refer to zenmap configuration',
            'ping'    : 'other ping parameters, refer to zenmap configuration',
            'script'  : 'other script parameters, refer to zenmap configuration',
            'target'  : 'other target parameters, refer to zenmap configuration',
            'source'  : 'other source parameters, refer to zenmap configuration',
            'other'   : 'other parameters, refer to zenmap configuration',
            'timing'  : 'other timing parameters, refer to zenmap configuration',
            'info'    : 'User do not need send all fields, will be none. All parameters will be spliced together. Please handle the conflicting fields.'
        }
        #print(help_message)
        return help_message


def nmapScan(args):
    # choose mode
    mode_choices = {
        'intense': ' -T4 -A -v ',
        'intense_udp': ' -sS -sU -T4 -A -v ',
        'intense_all_tcp': ' -p 1-65535 -T4 -A -v ',
        'intense_no_ping': ' -T4 -A -v -Pn ',
        'ping': ' -sn ',
        'quick': ' -T4 -F ',
        'quick_plus': ' -sV -T4 -O -F --version-light ',
        'quick_trace': ' -sn --traceroute ',
        'regular': ' ',
        'slow_comp': ' -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)" '
    }

    host = args.pop('host')
    port = args.pop('port')
    mode = args.pop('mode')

    if mode is not None:
        arguments = mode_choices[mode]
    else:
        arguments = ''

    for v in args.values():
        if v is not None:
            arguments += " "
            arguments += v

    # use flask restful api error handing, no need try catch
    nm = nmap.PortScanner()
    result = nm.scan(host, port, arguments, True)
    
    return result


api.add_resource(NmapReq, '/nmap/api/v1.0')

if __name__ == '__main__':
    app.run(debug=False)
