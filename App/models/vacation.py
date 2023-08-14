from App.database import db


class Vacation(db.Model):
    __tablename__ = 'vacations'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id=db.Column(db.Integer, db.ForeignKey('employees.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    # status = db.Column(db.String(20), default='Pending')
    vacationNum= db.Column(db.Integer, nullable=True)

    def __init__(self,employee_id, start_date, end_date, vacationNum):
        self.employee_id=employee_id
        self.start_date=start_date
        self.end_date=end_date
        self.vacationNum=vacationNum

    def get_json(self):
        return{
            'id':self.id,
            'employee_id': self.employee_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'vacationNum': self.vacationNum,
        }

    # def __repr__(self):
    #     return f"Vacation(id={self.id}, employee_id={self.employee_id}, start_date={self.start_date}, end_date={self.end_date})"