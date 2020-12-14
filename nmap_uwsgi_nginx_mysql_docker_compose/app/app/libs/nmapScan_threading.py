import nmap

from app.models.scanModel import ScanModel
from app.models.reportModel import ReportModel


def nmapScan_threading(app, host, port, arguments, scan_id):
    # start scan
    try:
        nm = nmap.PortScanner()
        # if the runner is not root, use sudo, put the last parameter to True
        # result = nm.scan(host, port, arguments, True)

        # if the runner is root, do not use sudo
        result = nm.scan(host, port, arguments, False)

    except nmap.nmap.PortScannerError as e:
        result = e.value
        code = 400
    except Exception:
        result = 'other error'
        code = 400
    else:
        code = 200

    print(code)
    # update scans status and finish time
    with app.app_context():
        scan = ScanModel.find_by_id(scan_id)
        if scan is not None:
            ScanModel.update_status_finish_time(scan_id)

            report = ReportModel(scan_id, str(result))
            report.add_to_db()









