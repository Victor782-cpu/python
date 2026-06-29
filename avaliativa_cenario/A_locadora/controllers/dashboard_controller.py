from flask import Blueprint, url_for, render_template

from models import ClienteLocadora, Locacao, Veiculo

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    return render_template("index.html",
    total_cliente = ClienteLocadora.query.count(),
    total_locacoes = Locacao.query.count(),
    total_veiculos = Veiculo.query.count())