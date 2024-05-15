# TODO Implement WifiStatus class as a singleton

from extensions import db
class WifiStatus(db.Model):
    __tablename__ = 'wifi_status'
    change_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    last_db_update = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    last_status_update = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    change_user = db.Column(db.String(50)) 

    def __init__(self):
        pass
    
    def save(self):
        db.session.add(self)
        db.session.commit()