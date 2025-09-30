from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<a href="/bye">Click me!</a>'

@app.route('/bye')
def bye():
    return 'bye world'


if __name__ == '__main__':
    app.run(debug=True, port=5001)#leave alone. this simply allows us to have a seperate testapp.y that we can run.


