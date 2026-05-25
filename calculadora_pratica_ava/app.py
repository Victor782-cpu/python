
from flask import Flask, render_template
from calculadora import calcular

cldr = Flask(__name__)

@cldr.route('/')
def index():
    return render_template('calculadora.html') 

if __name__ == "__main__":
     cldr.run(debug=True)