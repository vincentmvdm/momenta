from flask import Flask, render_template, request,redirect
import os

app = Flask(__name__)

print app.root_path

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug=True
    app.run()
