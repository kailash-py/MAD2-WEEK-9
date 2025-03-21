from flask import Flask, jsonify 
from worker import celery_init_app
from task import add
from celery.result import AsyncResult
app = Flask(__name__)

celery_app = celery_init_app(app)   # Initialize Celery


@app.route('/')
def home():
    return 'test'


@app.route("/execute_add")
def execute_add():
    add.delay(10, 20)
    return { "message":"Task added to queue"}

@app.route('/long-task')                    #trigger a long task
def execute_long():
    task = add.delay(30, 40)                #Async task
    return jsonify ({"task_id": task.id})


@app.route('/check/<task_id>')  
def check_task(task_id):
    asynch_task = add.AsyncResult(task_id)  # Get the task
    
    if asynch_task.ready():                 # Check if task is ready
        return jsonify({ "result": asynch_task.result}), 200
    else:
        return "Task is not ready", 425
     
if __name__ == '__main__':                  # Ensure this file is being run directly and not from a different module
    app.run(debug=True)
    