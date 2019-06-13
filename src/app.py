from _init_ import app

@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()