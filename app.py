from flask import Flask, render_template
from graph1 import js, div, cdn_jss
from graph2 import js1, div1, cdn_jss1
from graph3 import js2, div2, cdn_jss2
from graph4 import js3, div3, cdn_jss3




app=Flask(__name__)

@app.route('/')
def index():

    return render_template("index.html", js=js, div=div, cdn_jss=cdn_jss)

@app.route('/graph2')

def index2():
    return render_template("graph2.html", js=js1, div=div1, cdn_jss=cdn_jss1)

@app.route('/graph3')

def index3():
    return render_template("graph2.html", js=js2, div=div2, cdn_jss=cdn_jss2)

@app.route('/graph4')

def index4():
    return render_template("graph2.html", js=js3, div=div3, cdn_jss=cdn_jss3)

if __name__ == '__main__': 
    app.run(debug=True) 