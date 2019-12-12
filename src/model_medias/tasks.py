from celery import task


@task()
def add(x, y):
    result = x + y
    return result
