from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/PC/Desktop/MyTodoApp/todo.db"
db = SQLAlchemy(app)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)



@app.route('/complate/<string:id>')
def complateTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complate == True:
        todo.complate == False
    else:
        Todo.complate == True"""
    todo.complate = not todo.complate

    db.session.commit()

    return redirect(url_for("index"))

@app.route('/delete/<string:id>')
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))



@app.route('/add',methods = ["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title = title,complate = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    complate = db.Column(db.Boolean)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
