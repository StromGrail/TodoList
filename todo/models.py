from datetime import date,datetime
from todo import db

'''
Title id ,Title , Description  , due-date  , Status
'''

class Task(db.Model):
    TitleId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(20), unique=True, nullable=False)
    Description = db.Column(db.String(20),  nullable=False)
    Status = db.Column(db.Boolean,default=True)
    DueDate = db.Column(db.Date,nullable=False ,default=datetime.now)
    AlertTime = db.Column(db.Integer, default=24)
    Is_delete = db.Column(db.Boolean, default=False)
    DeleteDate = db.Column(db.Date,default='')
    subtask = db.relationship('Subtask',  lazy=True)
    def __repr__(self):
        return "Task('{}', '{}','{}','{}','{}','{}','{}','{}')".format(self.TitleId,self.Title,self.Description,self.Status,self.DueDate,self.AlertTime,self.Is_delete,self.DeleteDate)

'''
fTitle id ,Subtask Title, Duration , due-date ,sub Status
'''

class Subtask(db.Model):
    Subid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    SubTitle = db.Column(db.String(100), nullable=False)
    SubDueDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    SubDescription = db.Column(db.String(100), nullable=False)
    UnderTitle= db.Column(db.Integer, db.ForeignKey('task.TitleId'), nullable=False)
    SubStatus = db.Column(db.Boolean,default=True)

    def __repr__(self):
    	return "Subtask('{}','{}', '{}','{}','{}','{}')".format(self.Subid,self.SubTitle,self.SubDueDate,self.SubDescription,self.SubStatus,self.UnderTitle)