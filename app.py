from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}- {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def welcome():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('form.html', alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    del_todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
        if request.method=='POST':
            title=request.form['title']
            desc=request.form['desc']
            upt_todo=Todo.query.filter_by(sno=sno).first()
            upt_todo.title=title
            upt_todo.description=desc
            db.session.add(upt_todo)
            db.session.commit()
            return redirect("/")
        upt_todo=Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', upt_todo=upt_todo)    

if __name__ == "__main__":
    app.run(debug=True)
