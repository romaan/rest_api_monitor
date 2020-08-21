from celery import Celery
import requests
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def updateBlog():
    response = requests.get("https://www.dollarmates.com")
    print(response.status_code)