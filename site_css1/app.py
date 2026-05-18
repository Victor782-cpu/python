from flask import Flask, render_template

site = Flask(__name__)

@site.route('/')
def index():
    return render_template("index.html") 

@site.route('/page1')
def page1():
    return render_template("page1.html") 

@site.route('/page2')
def page2():
    return render_template("page2.html") 
@site.route('/page3')
def page3():
    return render_template("page3.html") 

if __name__ == '__main__':
    site.run(debug=True)