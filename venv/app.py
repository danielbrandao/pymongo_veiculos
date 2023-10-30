from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.veiculos
collection_carros = db.carros

# Endpoint para página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Lista os veículos cadastrados
@app.route("/lista")
def listar():
    retorno_carros = list(collection_carros.find())
    return render_template("listar.html", carros = retorno_carros)

# Formulário de cadastro de novo veículo
@app.route("/cadastra")
def insere_veiculo():
    return render_template("cadastrar.html")

# Cadastro do veículo no BD
@app.route("/cadastrar_bd", methods=['POST'])
def cadastra_veiculo_bd():
    carro = {
        'marca': request.form['marca'],
        'modelo': request.form['modelo'],
        'ano': request.form['ano'],
        'preco': request.form['preco'],
        'categoria': request.form['categoria']
    }
    collection_carros.insert_one(carro)
    return redirect("/lista")

# Formulário de alteração do veículo
@app.route("/editar/<id>")
def form_editar():
    carro = collection_carros.find_one({"_id": ObjectId(id)})
    return render_template("editar.html", carro=carro)

# Alteração do veículo no banco
@app.route("/carros/<id>/editar", methods=['POST','GET'])
def editar(id):
    if request.method == "POST":
        filtro = {"_id": ObjectId(id)}
        novo_valor = {
            "$set": {
                'marca': request.form['marca'],
                'modelo': request.form['modelo'],
                'ano': request.form['ano'],
                'preco': request.form['preco'],
                'categoria': request.form['categoria']
            }
        }
        collection_carros.update_one(filtro, novo_valor)
        return redirect("/lista")
    else:
        carro = collection_carros.find_one({"_id": ObjectId(id)})
        return render_template("editar.html", carro=carro)

# Exclusão do veículo no banco
@app.route("/carros/<id>/excluir")
def excluir(id):
    filtro = {"_id": ObjectId(id)}
    collection_carros.delete_one(filtro)
    return redirect("/lista")

# Visualizar o veículo individualmente
@app.route("/carro/<id>")
def contato(id):
    filtro = {"_id": ObjectId(id)}
    carros = collection_carros.find(filtro)
    return render_template("veiculo.html", carros = carros)

if __name__ == '__main__':
    app.run(debug=True)


