from flask import render_template

def index():
    return render_template('index.html')

def services():
    return render_template('services.html')

def ngo():
    return render_template('ngo.html')

def upload():
    return render_template('upload.html')

def result():
    return render_template('result.html')
    
def search():
    return render_template('search.html')