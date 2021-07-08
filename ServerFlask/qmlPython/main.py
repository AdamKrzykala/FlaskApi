# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_Task = ToDo(content=task_content)

        try:
            db.session.add(new_Task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    #db.create_all()
    appMain = QGuiApplication(sys.argv)
#    engine = QQmlApplicationEngine()
#    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
#    if not engine.rootObjects():
#        sys.exit(-1)
    app.run(debug=True)
    sys.exit(appMain.exec())
