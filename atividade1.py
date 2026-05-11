from flask import Flask

drtr = Flask(__name__)

@drtr.route('/')
def decorator():
    return 'Um decorator em Python é uma função que modifica ou estende o comportamento de outra função, método ou classe sem alterar seu código-fonte original.'

@drtr.route('/praq')
def decorator1():
    return 'Decorators em Python servem para modificar ou estender o comportamento de funções, métodos ou classes de forma elegante, sem alterar o código original.'

@drtr.route('/como')
def decorator2():
    return 'Como Criar e Utilizar um Decorator \n 1. Defina a função decoradora: Ela deve receber a função original (func) como argumento. \n\n 2. Crie uma função interna (wrapper): Esta função embrulha a original, permitindo executar códigos antes ou depois dela. \n\n Retorne a função interna: O decorador retorna a função (wrapper)' 

if __name__ == '__main__':
    drtr.run(debug=True)