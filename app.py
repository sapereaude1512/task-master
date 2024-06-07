from flask import Flask, render_template, url_for, request, redirect
# or: import flask.Flask --> flask is a package, Flask is a class
# render_template is a function
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# __name__ is file (in this case: app.py) environment variable and when runned have the value of __main__
# when importing another file in this one, value of __name__ is the name of the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# initialise database with the settings from the app

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # user will not be able to create a new task and then just leave the content of that task empty
    completed = db.Column(db.Integer, default=0)
    # ignore line above because completed column is never used
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self): # returning string
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # pass # do staff there
        # return 'Hello'
        task_content = request.form['content'] # id of the input in html is content
        new_task = Todo(content=task_content)
        try: # push it to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # look at all of the database contents in order they were created
        # .first() would be showing the most recent if we are sorting by date
        return render_template('index.html', tasks=tasks) # just looking at the page

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue with deleting your task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)