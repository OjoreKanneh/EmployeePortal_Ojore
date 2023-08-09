from App.database import db


class Vacation(db.Model):
    __tablename__ = 'vacations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')

    employee_id=db.Column(db.Integer, db.ForeignKey('employees.id'), unique=True)
    employee=db.relationship('Emplolyee',back_populates='vacation')
    
    # user = db.relationship('User', backref='vacations')

    def __repr__(self):
        return f"Vacation(id={self.id}, user_id={self.user_id}, start_date={self.start_date}, end_date={self.end_date}, status={self.status})"