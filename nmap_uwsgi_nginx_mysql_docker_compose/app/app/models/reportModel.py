from datetime import datetime

from app.libs.database import db


class ReportModel(db.Model):
    # ScanModel对应的表格： scans
    __tablename__ = 'reports'

    #
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scan_id = db.Column(db.Integer)
    result = db.Column(db.Text)

    def __init__(self, scan_id, result):
        self.scan_id = scan_id
        self.result = result


    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_id(cls, scan_id):
        # find
        return cls.query.filter_by(scan_id=scan_id).first()

    @classmethod
    def delete_by_id(cls, id):
        #print('delete report')
        # db.session.delete(cls.query.filter_by(scan_id=id).first())
        # db.session.commit()
        cls.query.filter_by(scan_id=id).delete()
        db.session.commit()
