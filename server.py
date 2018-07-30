from flask import Flask, session, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return   render_template('index.html')

if __name__ == '__main__':
    app.run()