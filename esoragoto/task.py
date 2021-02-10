@app.task(name='tasks.get_result')
def get_result(args):
    s = call(args)