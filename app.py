from flask import Flask,redirect,request,render_template

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mytodo.db'

db= SQLAlchemy(app)
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(200),nullable=False)
    desc =db.Column(db.String(500),nullable=False)
    date_created =db.Column(db.DateTime, default=datetime.now(),nullable=True)





with app.app_context():
    db.create_all()



@app.route("/",methods=['GET','POST'])
def home():

    if request.method == 'POST':

        title=request.form.get('title')
        desc=request.form.get('desc')

        todo=Todo(title=title,desc=desc)

        db.session.add(todo)
        db.session.commit()


    alltodo=Todo.query.all()
    
    return render_template('home.html',alltodo=alltodo)

@app.route("/delete/<string:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=int(sno)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<string:sno>",methods=["GET","POST"])
def update(sno):

    
    if request.method=="POST":

        

        title=request.form.get("update_title")
        desc=request.form.get("update_desc")

        todo=Todo.query.filter_by(sno=int(sno)).first()
        
        
        todo.title = title
        todo.desc = desc
        todo.date_created = datetime.now()


        # todo.title=title
        # todo.desc=desc
        # todo.date_created=datetime.now()

        db.session.commit()
        return redirect("/")
        # return redirect("/")
    

    todo=Todo.query.filter_by(sno=int(sno)).first()
    





    return render_template("update.html",todo=todo,sno=sno  )





if __name__ == '__main__':
    app.run(debug=True)


