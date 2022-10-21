from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB creation
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Table creation
class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    completed = db.Column(db.Integer, nullable=False)


#with app.app_context():
db.create_all()


@app.route('/')
def home():
    all_todo = db.session.query(TODO).all()
    return render_template("index.html", todo_list=all_todo, edit=False)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_todo = TODO(
            title=request.form["new_todo"],
            completed=0,
        )
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        todo_to_edit = TODO.query.get(request.form['id'])
        todo_to_edit.title = request.form["edit_todo"]
        db.session.commit()
        return redirect(url_for('home'))

    todo_to_edit = TODO.query.get(request.args.get('id'))
    return render_template("index.html", edit=True, todo=todo_to_edit)


@app.route("/done_undo")
def done_undo():
    todo_to_update = TODO.query.get(request.args.get('id'))

    if todo_to_update.completed == 1:
        todo_to_update.completed = 0
    else:
        todo_to_update.completed = 1

    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete")
def delete():
    todo_to_delete = TODO.query.get(request.args.get('id'))
    db.session.delete(todo_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
