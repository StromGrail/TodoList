from flask import render_template, url_for, flash, redirect,request
from todo import app, db
from todo.forms import AddTask
from todo.models import Task, Subtask
from datetime import datetime,timedelta
from sqlalchemy import exc,desc

@app.route('/all',methods=['GET'])
def showDatabaseValue():
    task=Task.query.all()
    return render_template('all.html',task=task)

@app.route('/', methods=['GET'])
@app.route('/<string:start>and<string:end>/' , methods = ['GET'])
@app.route('/and/' , methods = ['GET'])
@app.route('/home/' , methods = ['GET'])
def home(start='',end=''):
    if start=='':
        task=Task.query.order_by(Task.DueDate).all()
    elif start=='overdue_':
        task = Task.query.filter(Task.Status==True).order_by(Task.DueDate).all()
    else:
        task = Task.query.filter(Task.DueDate.between(start,end)).order_by(Task.DueDate).all()
    
    for t in task:
        hard_delete(t.TitleId)

    return render_template('index.html',task=task)


@app.route('/', methods=['POST'])
@app.route('/home/' , methods = ['POST'])
@app.route('/<string:start>and<string:end>/' , methods = ['POST'])
def my_form_post(start='',end=''):
    if request.method == 'POST' :
        result = request.form
        print("w", result)
        for key, value in result.items() :
            if key == 'Title':
                title = value
            elif key == 'Description':
                desc = value
            elif key == 'DueDate':
                duedate = datetime.strptime( value, "%Y-%m-%d" )
            else:
                alert= value

        task = Task(Title = title, Description = desc, DueDate = duedate,AlertTime=alert,DeleteDate=datetime.now())
        try:
            db.session.add(task)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
    task = Task.query.all()
    return redirect(url_for('home',start=start,end=end))


@app.route('/delete/<int:titleId>', methods=['POST'])
def delete_title(titleId):
    task = Task.query.get(titleId)
    task.Is_delete, task.DeleteDate = True, datetime.now()
    db.session.commit()
    return redirect(url_for('home'))

def hard_delete(TitleId):
    title = Task.query.get_or_404(TitleId)
    if title.Is_delete==True and datetime.now().date()-timedelta(days=30) >= title.DeleteDate:  
        subtask = Subtask.query.filter(Subtask.UnderTitle==title.TitleId).all()
        for s in subtask:
            db.session.delete(s)
        db.session.delete(title)
        db.session.commit()
    

@app.route('/subtask/<int:titleId>' , methods=['POST','GET'])
def subtask_title(titleId):
    print("Subtask",titleId)
    if request.method == 'POST' :
        result = request.form
        print("w", result)
        title=desc=''
        for key, value in result.items() :
            if key == 'SubTitle':
                title = value
            elif key == 'Description':
                desc = value
        if title!='':
            task=Task.query.get_or_404(titleId)
            duedate = task.DueDate
            subtask = Subtask(SubTitle = title, SubDescription = desc, SubDueDate = duedate,UnderTitle=titleId)
            try:
                db.session.add(subtask)
                db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()
    task = Subtask.query.filter(Subtask.UnderTitle==titleId).all()
    return render_template('subtaskindex.html',task=task)


@app.route('/Subtaskdelete/<int:UnderTitleid>_<int:Subid>', methods=['POST'])
def delete_subtitle(UnderTitleid,Subid):
    title = Subtask.query.get_or_404(Subid)
    db.session.delete(title)
    db.session.commit()
    return redirect(url_for('subtask_title',titleId=UnderTitleid))


@app.route('/showtask', methods=['POST'])
def showTask():
    select = request.form.getlist('selectVal')
    print(datetime.now()-timedelta(days=datetime.now().weekday()) )
    if select[0]=='All Task':
        return redirect( url_for('home') )
    elif select[0]=="Today":
        s=datetime.now() -timedelta(days=1)
        e=s+timedelta(days=1)
        print(s,' ',e)
    elif select[0]=="This Week":
        s=datetime.now()-timedelta(days=datetime.now().weekday())
        e=s+timedelta(days=6)
        print(s,' w ',e )
    elif select[0]=="Next Week":
        s=datetime.now()-timedelta(days=datetime.now().weekday())+timedelta(days=6)
        e=s+timedelta(days=6)
    else:
        s,e='overdue_','_pending'
    return redirect(url_for('home',start=s,end=e))

@app.route('/status/<int:titleId>' , methods=['POST','GET'])
def status_title(titleId):
    title = Task.query.get_or_404(titleId)
    title.Status^=True
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/substatus/<int:UnderTitleid>_<int:Subid>' , methods=['POST','GET'])
def substatus_title(UnderTitleid,Subid):
    stask = Subtask.query.get_or_404(Subid)
    print('Before',stask.SubStatus)
    stask.SubStatus^=True
    print('After',stask.SubStatus)
    db.session.commit()
    return redirect(url_for('subtask_title',titleId=UnderTitleid))


@app.route('/searchtitle',methods=['POST'])
def searchtitle():
    select = request.form.getlist('search')
    task = Task.query.filter(Task.Title == select[0] ).all()
    print(task)
    for t in task:
        print(t)
    return render_template('index.html',task=task)


