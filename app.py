from flask import Flask, render_template, request
from calculadora import calcular
cldr = Flask(__name__)


@cldr.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return calcular()
    return render_template('calculadora.html', etapas = '', resultados = '')

if __name__ == "__main__":
    cldr.run(debug=True)