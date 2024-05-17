from extensions import db


class WifiStatus(db.Model):
    __tablename__ = 'wifi_status'
    change_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    last_db_update = db.Column(
        db.DateTime(),
        nullable=False,
        default=db.func.current_timestamp().op('AT TIME ZONE')('EEST'),
        onupdate=db.func.current_timestamp().op('AT TIME ZONE')('EEST')
    )
    last_status_update = db.Column(
        db.DateTime(),
        nullable=False,
        default=db.func.current_timestamp().op('AT TIME ZONE')('EEST'),
        onupdate=db.func.current_timestamp().op('AT TIME ZONE')('EEST')
    )
    change_user = db.Column(db.String(50)) 

    def __init__(self):
        pass
    
    def save(self):
        db.session.add(self)
        db.session.commit()