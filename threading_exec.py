from flask import Flask
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(2)

app = Flask(__name__)
a=111

@app.route('/jobs')
def run_jobs():
    executor.submit(some_long_task1)
    executor.submit(some_long_task2, 'hello', 123)
    executor.submit(some_long_task3)

    print(a)

    return 'Two jobs was launched in background!'


def some_long_task1():
    print("Task #1 started!")
    sleep(10)
    print("Task #1 is done!")


def some_long_task3():
    print("Task #3 started!")
    sleep(15)
    print("Task #3 is done!")


def some_long_task2(arg1, arg2):
    print("Task #2 started with args: %s %s!" % (arg1, arg2))
    sleep(5)
    print("Task #2 is done!")


if __name__ == '__main__':
    app.run()