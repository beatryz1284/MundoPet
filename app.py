from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mundo_pet.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco
db = SQLAlchemy(app)


# =========================
# MODELO PET
# =========================

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    tutor = db.Column(db.String(100))


# =========================
# PÁGINA INICIAL
# =========================

@app.route("/")
def inicio():
    return render_template("index.html")


# =========================
# CADASTRAR PET
# =========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        especie = request.form["especie"]
        raca = request.form["raca"]
        idade = request.form["idade"]
        tutor = request.form["tutor"]

        novo_pet = Pet(
            nome=nome,
            especie=especie,
            raca=raca,
            idade=idade,
            tutor=tutor
        )

        db.session.add(novo_pet)
        db.session.commit()

        return redirect(url_for("pets"))

    return render_template("cadastro.html")


# =========================
# CONSULTAR PETS
# =========================

@app.route("/pets")
def pets():

    lista_pets = Pet.query.all()

    return render_template(
        "pets.html",
        pets=lista_pets
    )


# =========================
# EDITAR PET
# =========================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    pet = Pet.query.get_or_404(id)

    if request.method == "POST":

        pet.nome = request.form["nome"]
        pet.especie = request.form["especie"]
        pet.raca = request.form["raca"]
        pet.idade = request.form["idade"]
        pet.tutor = request.form["tutor"]

        db.session.commit()

        return redirect(url_for("pets"))

    return render_template(
        "editar.html",
        pet=pet
    )


# =========================
# EXCLUIR PET
# =========================

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):

    pet = Pet.query.get_or_404(id)

    db.session.delete(pet)
    db.session.commit()

    return redirect(url_for("pets"))


# =========================
# INICIAR APLICAÇÃO
# =========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)