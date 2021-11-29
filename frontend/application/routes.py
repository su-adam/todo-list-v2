from application import app
from application.forms import TaskForm
from flask import render_template, request, redirect, url_for, jsonify
import requests

backend_host = "todo-app_backend:5000"

@app.route('/')
@app.route('/home')
def home():
    all_tasks = requests.get("http://{backend_host}:5000/read/allTasks").json()
    app.logger.info(f"Tasks: {all_tasks}")
    return render_template('index.html', title="Home", all_tasks=all_tasks["tasks"])

@app.route('/create/task', methods=['GET','POST'])
def create_task():
    form = TaskForm()

    if request.method == "POST":
        response = requests.post(
            "http://{backend_host}:5000/create/task",
            json = {"description" : form.description.data}
        )
        app.logger.info(f"Response: {response.data}")
        return redirect(url_for('home'))

    return render_template("create_task.html", title="Add a new Task", form=form)



@app.route('/update/task/<int:id>', methods=['GET','POST'])
def update_task(id):
    form = TaskForm()
    task = requests.get(f"http://{backend_host}:5000/read/task{id}").json()
    app.logger.info(f"Task : {task}")

    if request.method == "POST":
        response = requests.post(
            f"http://{backend_host}:5000/update/task/{id}",
            json = {"description" : form.description.data}
        )
        return redirect(url_for('home'))

    return render_template('update_task.html', task=task, form=form)

# @app.route('/delete/task/<int:id>')
# def delete_task(id):
#     task = Tasks.query.get(id)
#     db.session.delete(task)
#     db.session.commit()
#     return redirect(url_for('home'))

# @app.route('/complete/task/<int:id>')
# def complete_task(id):
#     task = Tasks.query.get(id)
#     task.completed = True
#     db.session.commit()
#     return redirect(url_for('home'))

# @app.route('/incomplete/task/<int:id>')
# def incomplete_task(id):
#     task = Tasks.query.get(id)
#     task.completed = False
#     db.session.commit()
#     return redirect(url_for('home'))